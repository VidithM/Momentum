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
	RID 	 string `json:"rid,omitempty"`
	Username string `json:"username,omitempty"`
	Password string `json:"password,omitempty"`
	Name 	 string `json:"name,omitempty"`
	Email	 string `json:"email,omitempty"`
}

func main() {
	ctx := context.Background()
	redisURI, _ := os.LookupEnv("REDIS_URI")
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
		fmt.Println("Received get request body:", string(reqBody))
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
			exists, err := redisClient.Exists(ctx, searchTerm).Result()
			if err != nil {
				http.Error(w, "Error querying Redis for existence of search term", http.StatusBadRequest)
				return
			}
			if exists != 1 {
				fmt.Printf("Requested user w/ search term %s does not exist\n", searchTerm)
				continue
			}
			userJson, err := redisClient.Get(ctx, searchTerm).Result()
			if err != nil {
				http.Error(w, "Error querying Redis for search term", http.StatusBadRequest)
				return
			}
			resContent = append(resContent, userJson)
		}
		// Convert the raw results into JSON
		resContentJson, err := json.Marshal(resContent)
		fmt.Println(string(resContentJson))
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
		fmt.Println("Received update request body:", string(reqBody))

		// Unpack into UserSchema struct
		var reqContent UserSchema
		err = json.Unmarshal(reqBody, &reqContent)
		if err != nil {
			http.Error(w, "Error decoding JSON", http.StatusBadRequest)
			return
		}

		// extract RID, email
		RID := reqContent.RID
		email := reqContent.Email
		// check if object already exists. If so, get it and update the fields specified in req
		exists, err := redisClient.Exists(ctx, RID).Result()
		if err != nil {
			http.Error(w, "Error querying Redis for existence of RID", http.StatusBadRequest)
			return
		}
		var resContent UserSchema
		if exists == 1 {
			// does exist; make resContent the existing object and update
			existingJson, err := redisClient.Get(ctx, RID).Result()
			if err != nil { 
				http.Error(w, "Error querying Redis for RID (RID exists)", http.StatusBadRequest)
			}
			err = json.Unmarshal([]byte(existingJson), &resContent) 
			if reqContent.RID != "" {
				resContent.RID = reqContent.RID
			}
			if reqContent.Username != "" {
				resContent.Username = reqContent.Username
			}
			if reqContent.Password != "" {
				resContent.Password = reqContent.Password
			}
			if reqContent.Name != "" {
				resContent.Name = reqContent.Name
			}
			if reqContent.Email != "" {
				resContent.Email = reqContent.Email
			}
		} else {
			// does not exist; make resContent the same as request
			resContent = reqContent
		}

		resContentJson, err := json.Marshal(resContent)
		err = redisClient.Set(ctx, RID, string(resContentJson), 0).Err()
		if err != nil {
			http.Error(w, "Error writing User to Redis", http.StatusBadRequest)
			return
		}
		err = redisClient.Set(ctx, email, string(resContentJson), 0).Err()
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