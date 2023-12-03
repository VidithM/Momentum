package main

import (
	"fmt"
	"context"
	"github.com/redis/go-redis/v9"
	"encoding/json"
	"io/ioutil"
	"net/http"
)

type UserRID struct {
	RID 	 string `json:"rid"`
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
	opt, err := redis.ParseURL("redis://default:ZE3TpP3ruji8BcTHIDZ7PZTZnI1lQFhk@redis-10664.c299.asia-northeast1-1.gce.cloud.redislabs.com:10664")
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
		// Unpack into UserRID struct
		var reqContent UserRID
		err = json.Unmarshal(reqBody, &reqContent)
		if err != nil {
			http.Error(w, "Error decoding JSON", http.StatusBadRequest)
			return
		}

		// Get the RID, query JSON from Redis
		RID := reqContent.RID
		userJson, err := redisClient.Get(ctx, RID).Result()
		if err != nil {
			http.Error(w, "Error querying Redis for RID", http.StatusBadRequest)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		fmt.Fprint(w, userJson)
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
		// extract RID, write to Redis
		RID := reqContent.RID
		err = redisClient.Set(ctx, RID, string(reqBody), 0).Err()
		if err != nil {
			http.Error(w, "Error writing User to Redis", http.StatusBadRequest)
			return
		}
	})

	port := 8080
	addr := fmt.Sprintf("localhost:%d", port)
	fmt.Printf("User microservice listening on http://%s\n", addr)
	err = http.ListenAndServe(addr, nil)

	if err != nil {
		fmt.Printf("Error: %s\n", err)
	}
}