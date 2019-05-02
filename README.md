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
This application is meant to provide a scalable, low-maintenance, 100% ODK 
compatible conversion service suitable for these applications. 

The above features are addressed as follows:

  * Scalable: no state is maintained between api requests allowing multiple
    servers to handle requests without coordination
  * Low-maintenance: the api is based on the same pyfxorm library as the ODK
    tools and attempts to "go with the flow" to rapidly handle ODK updates
  * 100% ODK compatible: the service is based on the same pyxform library 
    specifically to decrease the opportunity for incompatibilities.

Additionally, validation is handled separately because:

  * Is useful outside of XLSForm conversion
  * It requires a completely different runtime, Java, and its own dependencies
  * Deployed separately, both services can benefit from the same benefits 
    listed above
 
## Requirements

To build this application, you'll need:

  * Docker

## Building

To build the application as a docker image, you just need to run the following from the project's root
directory:

```
docker build .
```

