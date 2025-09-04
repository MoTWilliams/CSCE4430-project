#include "class.h"

#include <iostream>
#include <string>

int main() {
    // Print the prompt
    std::cout << "\nEnter a message\n> ";
    
    // Get input
    std::string msg = "";
    std::getline(std::cin, msg);

    Thing thing;
    thing.setMsg(msg);

    std::cout << "You entered \"" << thing.getMsg() << "\"\n\n";

    #if DEBUG
        std::cout << "This is how to use DEBUG mode\n\n";
    #endif

    return 0;
}