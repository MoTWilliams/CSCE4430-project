#ifndef THING_H
#define THING_H

#include <string>

class Thing {
private:
    std::string message;
public:
    Thing();
    ~Thing();

    void setMsg(std::string msg);
    std::string getMsg();
};

#endif