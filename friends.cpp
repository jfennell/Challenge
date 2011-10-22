#include <iostream>
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

	/*
	for(std::list<std::string>::const_iterator res = results.begin();
		res != results.end();
		++res)
	{
		std::cout << *res << std::endl;
	}
	*/
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
	}
	return all_friends;
}


int main() 
{
	std::cout << "Hello world" << std::endl;
	all_one_edits("");
	std::cout << "---" << std::endl;
	all_one_edits("X");
	std::cout << "---" << std::endl;
	all_one_edits("XX");
	return 0;
}
