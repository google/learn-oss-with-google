package main

import (
	"fmt"
	"net/http"
	"os"
	"time"
)

var version = "0.0.2"

func indexHandler(w http.ResponseWriter, req *http.Request) {
	localFile, err := os.ReadFile("/data/hello-world.txt")
	if err != nil {
		fmt.Printf("couldn't read file %v\n", err)

	}
	fmt.Fprintf(w, "<h1>hello world :) </h1> \n Version %s\n File Content:%s", version, localFile)
}

func headersHandler(w http.ResponseWriter, req *http.Request) {

	for name, headers := range req.Header {
		for _, h := range headers {
			fmt.Fprintf(w, "%v: %v\n", name, h)
		}
	}
}

func main() {

	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/headers", headersHandler)

	welcomeText := fmt.Sprintf("%s Starting example version %s, Listening on port 8080 ...", time.Now().String(), version)
	fmt.Println(welcomeText)
	http.ListenAndServe(":8080", nil)
}
