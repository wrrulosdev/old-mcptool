# Fakeproxy Guide

## What is Fakeproxy?
The fakeproxy command creates a velocity proxy server with my RFakeProxy plugin. The function of the mentioned plugin is to capture all user data that enters the MCPTool proxy server (messages, commands and connections). In addition to allowing the owner of the proxy to execute commands on the accounts of other people who have entered the fake proxy.

## How to use Fakeproxy?
To use the fakeproxy command in MCPTool, you only need to use the command

```bash
fakeproxy <ip:port/domain> <forwarding-mode>
```

## What is forwarding-mode?
https://docs.papermc.io/velocity/player-information-forwarding

## Where does it work?
Mainly, fakeproxy works on non-premium or semi-premium servers. In the case of semi-premium servers, it will only work with usernames that do not have /premium (or similar) enabled. 

If you try to use fakeproxy on a premium or semi-premium server with a user who does NOT have to use the /login command (or similar), the speed proxy will not let the user in, saying that the backend server is in online mode.

## What is the admin key?
The administrator key is what will allow you to use the administrator commands within the fakeproxy. You just have to copy the administrator key and enter it in the Minecraft chat (being inside the fakeproxy). Then you can run the fakeproxy commands. (**#help**)

## Fakeproxy commands
- **#help** - Shows the help menu.
- **#list** - Shows the list of users connected to the fakeproxy.
- **#send <username> <message/command>** - Send a message or command from the specified user's account.

## How can I share my fakeproxy server IP with users outside my network?
By default, fakeproxy only creates a local proxy in the port 33330. To expose your port you can use services like [ngrok](https://ngrok.com/), [pinggy](https://pinggy.io/) or open your router's port and use its IP address.
