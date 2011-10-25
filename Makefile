# g++ -O3 -pedantic -Wall -Wextra friends_overoptimized.cpp -o friends_extra

CXXFLAGS = -pedantic -Wall -Wextra
OPTIMIZE = -O3
DEBUG = -g

all: friends_extra friends

friends: friends.cpp
	g++ $(OPTIMIZE) $(CXXFLAGS) $< -o $@

friends_extra: friends_overoptimized.cpp
	g++ $(OPTIMIZE) $(CXXFLAGS) $< -o $@


clean:
	rm friends
	rm friends_extra

.PHONY: all clean
