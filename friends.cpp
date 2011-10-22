#include <iostream>
#include <fstream>
#include <list>
#include <queue>
#include <set>
#include <string>

std::string ALPHABET("abcdefghijklmnopqrstuvwxyz");

/**
 * Generate all single edits for `word` assuming the
 * alphabet is [a-z].
 */
std::list<std::string> all_one_edits(std::string word)
{
	size_t n = word.length();
	std::list<std::string> results;

	for(size_t i = 0; i < n; ++i)
	{
		std::string prefix = word.substr(0, i);
		for(std::string::const_iterator c = ALPHABET.begin();
			c < ALPHABET.end();
			++c)
		{
			// Replace
			results.push_back(prefix + *c + word.substr(i+1));
			// Insert
			results.push_back(prefix + *c + word.substr(i));

		}
		// Delete
		results.push_back(prefix + word.substr(i+1));
	}

	// Inserting at the ever end of the string
	for(std::string::const_iterator c = ALPHABET.begin();
		c < ALPHABET.end();
		++c)
	{
		results.push_back(word + *c);
	}

	return results;
}


/**
 * Find the closure of the friend relation over dictionary starting from start.
 */
std::set<std::string> find_friend_closure(std::string start, std::set<std::string> dictionary)
{
	std::set<std::string> all_friends;
	all_friends.insert(start);
	std::queue<std::string> expand_queue;
	expand_queue.push(start);

	size_t count = 0;
	while (!expand_queue.empty())
	{
		std::string word = expand_queue.front();
		expand_queue.pop();

		std::list<std::string> edits = all_one_edits(word);
		for(std::list<std::string>::const_iterator edit = edits.begin();
			edit != edits.end();
			++edit)
		{
			if (dictionary.count(*edit) > 0 && all_friends.count(*edit) == 0)
			{
				expand_queue.push(*edit);
				all_friends.insert(*edit);
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


std::set<std::string> load_dictionary(const char* path)
{
	std::set<std::string> dictionary;

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
	std::set<std::string> dictionary = load_dictionary("word.list");
	std::set<std::string> friends = find_friend_closure(word, dictionary);
	std::cout << word << " has " << friends.size() << " friends." << std::endl;
	return 0;
}
