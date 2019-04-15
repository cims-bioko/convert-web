# CIMS Convert Web

A web service for converting XLSForms to ODK-compliant xforms. It provides a 
means of conversion using HTTP protocols. It is intended to be used by web 
applications, not by humans, and it focuses on conversion. It *does not* 
attempt to handle validation. Instead it leverages the separate validation
service.

## Why?

The existing ODK tool, XLSForm Online, delivers an all-in-one conversion 
service for human users. Certain characteristics, directly derived from that 
goal, makes it unsuitable for programmatic usage for other web applications.
This application is meant to provide a high-performance, highly-scalable, 
conversion service suitable for these types of applications.
 
## Requirements

To build this application, you'll need:

  * Docker

## Building

To build the application as a docker image, you just need to run the following from the project's root
directory:

```
docker build .
```

