### IRCLogger

IRCLogger is written in Python without using any third party modules.

### Copyright, License and Authors 
Copyright (c) 2012 Muneeb Shaikh <iammuneeb@gmail.com>
License: GPLv3+
## TODOs

### High
* Parse the logfile and generate html page to display online.
    - option for dark and light theme
    - Filter to follow the discussion.
      e.g. To follow discussion between person X and person Y, add two text fields to filter other clutter.
    - Homepage displaying calender view, from where we can browse the previous logs.

### Medium
* Redesign the IRCLogBot class as IRCBot to contain basic minimum functionality of connecting, saving raw log, disconnecting.
    - Then create special Bots for particular work by inheriting from main IRCBot class
        + ClassBot (for conducting classroom sessions)
        + LogBot (for pure logging purpose, this is what we have now, still it does not log raw messages)
        + DictBot (ask a definition of word, it'll tell you definition, something of [this](http://reversehack.in/index.php/programming/36-tutorial/65-writing-useful-p-xchat-plugin-dictbot-in-python-awesomeness-in-not-more-than-15-lines-and-15-minutes-) type ) 
        + SearchBot (still thinking)
        + AIBot (heard of cleverbot?, something like that/similar)

