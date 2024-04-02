package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/trendmicro/tm-v1-fs-golang-sdk/client"
)

var (
	apiKey = os.Getenv("V1_KEY")
	region = os.Getenv("REGION")
	port   = os.Getenv("PORT")
)

func uploadFile(c *client.AmaasClient) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		file, header, err := r.FormFile("file")
		if err != nil {
			fmt.Println("Error Retrieving the File:", err)
			http.Error(w, "Error retrieving the file", http.StatusBadRequest)
			return
		}
		defer file.Close()

		t := r.URL.Query().Get("tags")
		tags := strings.Split(t, ",")
		if len(tags) == 0 {
			tags = nil
		}
		if len(tags) > 8 {
			log.Fatalf("tags accepts up to 8 strings")
			http.Error(w, "Error reading the file", http.StatusUnprocessableEntity)
			return
		}

		fileBytes, err := io.ReadAll(file)
		if err != nil {
			fmt.Println("Error reading the file:", err)
			http.Error(w, "Error reading the file", http.StatusInternalServerError)
			return
		}

		resp, err := c.ScanBuffer(fileBytes, header.Filename, tags)
		if err != nil {
			http.Error(w, "Error scanning the file", http.StatusUnprocessableEntity)
			return
		}

		w.WriteHeader(http.StatusOK)
		w.Write([]byte(resp))
	}
}

func main() {
	newClient, err := client.NewClient(apiKey, region)
	if err != nil {
		log.Fatalf("error creating v1 client: %v", err)
	}

	http.HandleFunc("/scan", uploadFile(newClient))
	fmt.Printf("Server started on :%v\n", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("error starting server: %v", err)
	}
	defer newClient.Destroy()
}
