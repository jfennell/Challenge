/**
 * Solve the causes challenge in go by repeatedly finding all 1-edit-away
 * words.
 */

package main

import (
	"os"
	"fmt"
	"strings"
	"io/ioutil"
)

func main() {
	path := "word.list"

	data, err := ioutil.ReadFile(path)
	if err != nil {
		fmt.Printf("Failed to open file at %s with error %s\n",
			path, err)
		os.Exit(1)
	}

	stringData := string(data)
	lines := strings.Split(stringData, "\n", -1)

	dictionary := make(map[string]bool)
	//alphabet := "abcdefghijklmnopqrstuvwxyz"
	//alphabet := {"a", "b"}

	numLines := len(lines)
	for i := 0; i < numLines; i++ {
		dictionary[lines[i]] = true
		//fmt.Printf("%s\n", lines[i])
	}

	word := "causes"
	allFriends := findFriendsClosure(word, dictionary)
	fmt.Printf("Found %d friends" , len(allFriends))
}

func findFriendsClosure(start string, dictionary map[string]bool) map[string]bool{
	allFriends := make(map[string]bool)
	toExpand := make(chan string, 100000)
	toExpand <- start

	var alphabet string = "abcdefghijklmnopqrstuvwxyz"

	count := 0
	for curr := range toExpand {
		for edit := range allSingleEdits(curr, alphabet) {
			_, inDict := dictionary[edit]
			_, inFriends := allFriends[edit]
			if inDict && !inFriends {
				toExpand <- edit
				allFriends[edit] = true
			}
		}

		count += 1
		if count > 0 && (count % 1000 == 0) {
			fmt.Printf("Expanded %d times, %d in the queue, %d friends so far.\n",
				count, len(toExpand), len(allFriends))
		}
	}
	return allFriends
}

func allSingleEdits(word, alphabet string) <-chan string {
	n := len(word)
	accum := make(chan string)

	go func() {
		for splitIdx := 0; splitIdx < n; splitIdx++ {
			for charIdx := 0; charIdx < 26; charIdx++ {
				char := string(alphabet[charIdx])
				accum <- word[:splitIdx] + char + word[splitIdx+1:]  // Replace
				accum <- word[:splitIdx] + word[splitIdx+1:]         // Delete
				accum <- word[:splitIdx] + char + word[splitIdx:]    // Insert
			}
		}
		// Finish the replace
		for charIdx := 0; charIdx < 26; charIdx++ {
			accum <- word + string(alphabet[charIdx])
		}

		close(accum)
	}()
	return accum
}


