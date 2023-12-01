package main

import (
	"fmt"
	_"context"
	"github.com/redis/go-redis/v9"
	_"encoding/json"
	"net/http"
)

func handleGet(w http.ResponseWriter, r *http.Request) {

}

func handleSet(w http.ResponseWriter, r *http.Request) {

}

func main() {
	http.HandleFunc("/get", handleGet)
	http.HandleFunc("/set", handleSet)

	opt, err := redis.ParseURL("redis://default:ZE3TpP3ruji8BcTHIDZ7PZTZnI1lQFhk@redis-10664.c299.asia-northeast1-1.gce.cloud.redislabs.com:10664")
	if err != nil {
		panic(err)
	}
	_ = redis.NewClient(opt)
	port := 8080
	addr := fmt.Sprintf("localhost:%d", port)
	fmt.Printf("Server listening on http://%s\n", addr)

	err = http.ListenAndServe(addr, nil)

	if err != nil {
		fmt.Printf("Error: %s\n", err)
	}
}