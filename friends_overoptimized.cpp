#include <iostream>
#include <fstream>
#include <list>
#include <queue>
#include <string>
#include <tr1/unordered_set>

typedef std::tr1::unordered_set<std::string> StringSet;

const std::string ALPHABET("abcdefghijklmnopqrstuvwxyz");

void check_and_add(
	const std::string& word,
	const StringSet& dictionary,
	StringSet& all_friends,
	std::queue<std::string>& expand_queue)
{
	// If the dict has the edit then it is a valid word,
	// and if all_friends doesn't have it then it still needs expansion
	if (dictionary.find(word) != dictionary.end() &&
		all_friends.find(word) == all_friends.end())
	{
		expand_queue.push(word);
		all_friends.insert(word);
	}
	
}


/**
 * Find the closure of the friend relation over dictionary starting from start.
 */
StringSet find_friend_closure(const std::string start, const StringSet dictionary)
{
	StringSet all_friends;
	all_friends.insert(start);
	std::queue<std::string> expand_queue;
	expand_queue.push(start);

	size_t count = 0;
	while (!expand_queue.empty())
	{
		std::string word = expand_queue.front();
		expand_queue.pop();

		size_t n = word.length();

		// Replace
		for(size_t i = 0; i < n; ++i)
		{
			char old_char = word[i];
			for(std::string::const_iterator c = ALPHABET.begin();
				c < ALPHABET.end();
				++c)
			{
				word[i] = *c;
				check_and_add(word, dictionary, all_friends, expand_queue);
			}
			word[i] = old_char;
		}

		// Delete
		if (n > 0) {
			char del_char = word[0];
			word.erase(0, 1);
			check_and_add(word, dictionary, all_friends, expand_queue);
			for(size_t i = 0; i < n-1; ++i)
			{
				char tmp = word[i];
				word[i] = del_char;
				del_char = tmp;
				check_and_add(word, dictionary, all_friends, expand_queue);
			}
			word.push_back(del_char);
		}

		// Insert
		word.insert(0, 1, 'X');
		for(size_t i = 0; i < n+1; ++i)
		{
			for(std::string::const_iterator c = ALPHABET.begin();
				c < ALPHABET.end();
				++c)
			{
				word[i] = *c;
				check_and_add(word, dictionary, all_friends, expand_queue);
			}
			if (i+1 <= n) {
				char tmp = word[i+1];
				word[i+1] = word[i];
				word[i] = tmp;
			}
		}

		++count;
		if (count > 0 && count % 1000 == 0) {
			std::cout
				<< "Expanded " << count << " times, "
				<< expand_queue.size() << " in the queue, "
				<< all_friends.size() << " friends so far."
				<< std::endl;
		}
	}
	return all_friends;
}


StringSet load_dictionary(const char* path)
{
	StringSet dictionary;

	std::ifstream file(path);
	if (file.is_open())
	{
		std::string line;
		while (file.good())
		{
			getline(file, line);
			dictionary.insert(line);
		}
	}
	else
	{
		std::cout << "Unable to open file" << std::endl;
	}

	return dictionary;
}


int main()
{
	std::string word = "causes";
	StringSet dictionary = load_dictionary("word.list");
	StringSet friends = find_friend_closure(word, dictionary);
	std::cout << word << " has " << friends.size() << " friends." << std::endl;
	return 0;
}
