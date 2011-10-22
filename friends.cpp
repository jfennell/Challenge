#include <iostream>
#include <string>

std::string ALPHABET("abcdefghijklmnopqrstuvwxyz");

void all_one_edits(std::string word)
{
	size_t n = word.length();

	for(int i; i < n; ++i)
	{
		for(std::string::const_iterator c = ALPHABET.begin();
			c < ALPHABET.end();
			++c)
		{
			// XXX: Missing 'empty' c
			std::cout 
			  << word.substr(0, i)
			  << *c
			  << word.substr(i+1)
			  << std::endl;
		}
	}

	for(int i; i < n+1; ++i)
	{
		for(std::string::const_iterator c = ALPHABET.begin();
			c < ALPHABET.end();
			++c)
		{
			std::cout
			  << word.substr(0, i)
			  << *c
			  << word.substr(i)
			  << std::endl;
		}
	}
}

int main() 
{
	std::cout << "Hello world" << std::endl;
	all_one_edits("");
	std::cout << std::endl << std::endl;
	all_one_edits("X");
	return 0;
}
