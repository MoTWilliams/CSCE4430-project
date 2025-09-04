#include "class.h"

#include <iostream>
#include <string>

Thing::Thing() {
    std::cout << "Constructor called\n\n";
}

Thing::~Thing() {
    std::cout << "Destructor called\n\n";
}

void Thing::setMsg(std::string msg) {
    message = msg;
}

std::string Thing::getMsg() {
    return message;
}