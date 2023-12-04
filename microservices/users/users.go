package main

import (
	"os"
	"fmt"
	"context"
	"github.com/redis/go-redis/v9"
	"encoding/json"
	"io/ioutil"
	"net/http"
)

type UserRequest struct {
	Terms	 []string `json:"terms"`
}

type UserSchema struct {
	RID 	 string `json:"rid"`
	Username string `json:"username"`
	Password string `json:"password"`
	Name 	 string `json:"name"`
	Email	 string `json:"email"`
}

func main() {
	ctx := context.Background()
	redisURI, ok := os.LookupEnv("REDIS_URI")
	if !ok {
		redisURI = "redis://default:ZE3TpP3ruji8BcTHIDZ7PZTZnI1lQFhk@redis-10664.c299.asia-northeast1-1.gce.cloud.redislabs.com:10664"
	}
	opt, err := redis.ParseURL(redisURI)
	if err != nil {
		panic(err)
	}
	redisClient := redis.NewClient(opt)
	
	http.HandleFunc("/getuser", func (w http.ResponseWriter, r *http.Request) {
		// Verify it's a GET request
		if r.Method != http.MethodGet {
			http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
			return
		}

		// Read request body as bytes
		reqBody, err := ioutil.ReadAll(r.Body)
		if err != nil {
			http.Error(w, "Error reading request body", http.StatusBadRequest)
			return
		}
		defer r.Body.Close()
		fmt.Println("Received request body:", string(reqBody))
		// Unpack into UserRequest struct
		var reqContent UserRequest
		err = json.Unmarshal(reqBody, &reqContent)
		if err != nil {
			http.Error(w, "Error decoding JSON", http.StatusBadRequest)
			return
		}
		
		// Populate raw result using all search terms
		var resContent []string
		for i := 0; i < len(reqContent.Terms); i++ {
			// Get the search term, query JSON from Redis
			searchTerm := reqContent.Terms[i]
			userJson, err := redisClient.Get(ctx, searchTerm).Result()
			if err != nil {
				http.Error(w, "Error querying Redis for RID", http.StatusBadRequest)
				return
			}
			resContent = append(resContent, userJson)
		}
		// Convert the raw results into JSON
		resContentJson, err := json.Marshal(resContent)
		if err != nil {
			http.Error(w, "Error encoding JSON", http.StatusBadRequest)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprint(w, string(resContentJson))
	})

	http.HandleFunc("/updateuser", func (w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
			return
		}

		// Read request body as bytes
		reqBody, err := ioutil.ReadAll(r.Body)
		if err != nil {
			http.Error(w, "Error reading request body", http.StatusBadRequest)
			return
		}
		defer r.Body.Close()
		fmt.Println("Received request body:", string(reqBody))
		// Unpack into UserSchema struct
		var reqContent UserSchema
		err = json.Unmarshal(reqBody, &reqContent)
		if err != nil {
			http.Error(w, "Error decoding JSON", http.StatusBadRequest)
			return
		}
		// extract RID, email, write to Redis
		RID := reqContent.RID
		email := reqContent.Email
		err = redisClient.Set(ctx, RID, string(reqBody), 0).Err()
		if err != nil {
			http.Error(w, "Error writing User to Redis", http.StatusBadRequest)
			return
		}
		err = redisClient.Set(ctx, email, string(reqBody), 0).Err()
		if err != nil {
			http.Error(w, "Error writing User to Redis", http.StatusBadRequest)
			return
		}
	})

	port := 8080
	addr := fmt.Sprintf("0.0.0.0:%d", port)
	fmt.Printf("User microservice listening on http://%s\n", addr)
	err = http.ListenAndServe(addr, nil)

	if err != nil {
		fmt.Printf("Error: %s\n", err)
	}
}