#include <iostream>
#include <fstream>
#include <list>
#include <queue>
#include <string>
#include <tr1/unordered_set>

typedef std::tr1::unordered_set<std::string> StringSet;

std::string ALPHABET("abcdefghijklmnopqrstuvwxyz");

/**
 * Generate all single edits for `word` assuming the
 * alphabet is [a-z].
 */
void all_one_edits(const std::string& word, std::list<std::string>& edits)
{
	size_t n = word.length();

	for(size_t i = 0; i < n; ++i)
	{
		std::string prefix = word.substr(0, i);
		std::string replace_tail = word.substr(i+1);
		std::string insert_tail = word.substr(i);

		// Delete - 'Replace' with no character
		edits.push_back(prefix + replace_tail);

		for(std::string::const_iterator c = ALPHABET.begin();
			c < ALPHABET.end();
			++c)
		{
			if (c == ALPHABET.begin()) {
				prefix.push_back(*c);
			} else {
				// XXX: Can I always safely do just this?
				prefix.replace(i, 1, 1, *c);
			}
			// Replace
			edits.push_back(prefix + replace_tail);
			// Insert
			edits.push_back(prefix + insert_tail);
		}
	}

	// Last insert: adding to the end of the string
	for(std::string::const_iterator c = ALPHABET.begin();
		c < ALPHABET.end();
		++c)
	{
		edits.push_back(word + *c);
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

		std::list<std::string> edits;
		all_one_edits(word, edits);
		for(std::list<std::string>::const_iterator edit = edits.begin();
			edit != edits.end();
			++edit)
		{
			// If the dict has the edit then it is a valid word,
			// and if all_friends doesn't have it then it still needs expansion
			//if (dictionary.count(*edit) > 0 && all_friends.count(*edit) == 0)
			// XXX Seems to be the slow bit (other order even worse!)
			if (dictionary.find(*edit) != dictionary.end() &&
				all_friends.find(*edit) == all_friends.end())
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
