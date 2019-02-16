# AvalonRestAgent.bundle

[![license](https://img.shields.io/github/license/ajtatum/AvalonRestAgent.bundle.svg)](https://github.com/ajtatum/AvalonRestAgent.bundle/blob/master/LICENSE)

This is a Plex rest API agent.
This allows users to implement your own rest API metadata server without implement the Plex agent.

## Requirements

* Able to implement your rest API metadata server with any language

## Install

```bash
cd /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/
git clone https://github.com/ajtatum/AvalonRestAgent.bundle.git
chown plex:plex AvalonRestAgent.bundle
service plexmediaserver restart
```

You need to enter Plex token and metadata server URL in setting.

## API Schema

[See here][schema]

## Frequently Asked Questions

**How do I implement an rest API metadata server?**

Read the [schema][schema] and implement it yourself. 
If you do not know how to do it, this agent is not designed for you.

**I do not want to open my metadata server to public. What should I do?**

There are two ways to do it.

1. Place the metadata server in the same LAN of Plex. Use LAN ip for the agent to access.
2. Implement HTTP basic authentication in your API server. Then, you can use http://username:password@example.com for the server address.

## Developer Notes

Here are some notes if you plan to fork the repository:

1. Plex uses Python version 2.7.12 on Linux machines.
     1. To verify this, install the [Plex WebTools Plugin](https://github.com/ukdtom/WebTools.bundle "Plex WebTools Plugin")
     2. Go to the "TechInfo" tool option and look for the "Python" key
2. To setup a virtual environment on Windows for Python 2.7.12, run:
    * C:\Python27\Scripts\virtualenv -p c:\Python27\python.exe env
3. To activate the virtual environment, run:
    * .\env\Scripts\activate

[schema]: https://ajtatum.github.io/AvalonRestAgent.bundle/