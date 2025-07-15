<!--
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020-25 https://prrvchr.github.io                                  ║
║                                                                                    ║
║   Permission is hereby granted, free of charge, to any person obtaining            ║
║   a copy of this software and associated documentation files (the "Software"),     ║
║   to deal in the Software without restriction, including without limitation        ║
║   the rights to use, copy, modify, merge, publish, distribute, sublicense,         ║
║   and/or sell copies of the Software, and to permit persons to whom the Software   ║
║   is furnished to do so, subject to the following conditions:                      ║
║                                                                                    ║
║   The above copyright notice and this permission notice shall be included in       ║
║   all copies or substantial portions of the Software.                              ║
║                                                                                    ║
║   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                  ║
║   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES                  ║
║   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.        ║
║   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY             ║
║   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,             ║
║   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE       ║
║   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                    ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
-->
# [![H2dbOOo logo][1]][2] Documentation

**Ce [document][3] en français.**

**The use of this software subjects you to our [Terms Of Use][4].**

# version [1.2.1][5]

## Introduction:

**H2dbOOo** is part of a [Suite][6] of [LibreOffice][7] ~~and/or [OpenOffice][8]~~ extensions allowing to offer you innovative services in these office suites.  

This extension allows you to use [H2 Database][9] in embedded mode, making the database portable (a single odb file).  
It allows you to take advantage of the [ACID][10] properties of the underlying [H2 Database][11] database.

Being free software I encourage you:
- To duplicate its [source code][12].
- To make changes, corrections, improvements.
- To open [issue][13] if needed.

In short, to participate in the development of this extension.  
Because it is together that we can make Free Software smarter.

___

## Requirement:

The H2dbOOo extension uses the jdbcDriverOOo extension to work.  
It must therefore meet the [requirement of the jdbcDriverOOo extension][14].

Additionally, due to [issue #156471][15] and following [PR#154989][16], the H2dbOOo extension requires **LibreOffice version 24.2.x** minimum to work.

___

## Installation:

It seems important that the file was not renamed when it was downloaded.  
If necessary, rename it before installing it.

- [![jdbcDriverOOo logo][17]][18] Install **[jdbcDriverOOo.oxt][19]** extension [![Version][20]][19]

    This extension is necessary to use H2 Database with all its features.

- ![H2dbOOo logo][21] Install **[H2dbOOo.oxt][22]** extension [![Version][23]][22]

Restart LibreOffice after installation.  
**Be careful, restarting LibreOffice may not be enough.**
- **On Windows** to ensure that LibreOffice restarts correctly, use Windows Task Manager to verify that no LibreOffice services are visible after LibreOffice shuts down (and kill it if so).
- **Under Linux or macOS** you can also ensure that LibreOffice restarts correctly, by launching it from a terminal with the command `soffice` and using the key combination `Ctrl + C` if after stopping LibreOffice, the terminal is not active (no command prompt).

After restarting LibreOffice, you can ensure that the extension and its driver are correctly installed by checking that the `io.github.prrvchr.H2dbOOo.Driver` driver is listed in the **Connection Pool**, accessible via the menu: **Tools -> Options -> LibreOffice Base -> Connections**. It is not necessary to enable the connection pool.

If the driver is not listed, the reason for the driver failure can be found in the extension's logging. This log is accessible via the menu: **Tools -> Options -> LibreOffice Base -> Embedded H2 Driver -> Logging Options**.  
The `H2dbLogger` logging must first be enabled and then LibreOffice restarted to get the error message in the log.

Remember to first update the version of the Java JRE or JDK installed on your computer, this extension need the new version of jdbcDriverOOo that requires **Java version 17 or later** instead of Java 11 previously.

___

## Use:

### How to create a new database:

In LibreOffice / OpenOffice go to File -> New -> Database...:

![H2dbOOo screenshot 1][24]

In step: Select database:
- select: Create a new database
- in: Emdedded database: choose: **Embedded H2 Driver**
- click on button: Next

![H2dbOOo screenshot 2][25]

In step: Save and proceed:
- adjust the parameters according to your needs...
- click on button: Finish

![H2dbOOo screenshot 3][26]

Have fun...

___

## How does it work:

H2dbOOo is an [com.sun.star.sdbc.Driver][27] UNO service written in Python.  
It is an overlay to the [jdbcDriverOOo][18] extension allowing to store the H2 database in an odb file (which is, in fact, a compressed file).

Its operation is quite basic, namely:

- When requesting a connection, several things are done:
  - If it does not already exist, a **subdirectory** with name: `.` + `odb_file_name` + `.lck` is created in the location of the odb file where all H2 files are extracted from the **database** directory of the odb file (unzip).
  - The [jdbcDriverOOo][18] extension is used to get the [com.sun.star.sdbc.XConnection][28] interface from the **subdirectory** path + `/H2`.
  - If the connection is successful, a [DocumentHandler][29] is added as an [com.sun.star.util.XCloseListener][30] and [com.sun.star.document.XStorageChangeListener][31] to the odb file.
  - If the connection is unsuccessful and the files was extracted in phase 1, the **subdirectory** will be deleted.
- When closing or renaming (Save As) the odb file, if the connection was successful, the [DocumentHandler][29] copies all files present in the **subdirectory** into the (new) **database** directory of the odb file (zip), then delete the **subdirectory**.

The main purpose of this mode of operation is to take advantage of the ACID characteristics of the underlying database in the event of an abnormal closure of LibreOffice.
On the other hand, the function: **file -> Save** has **no effect on the underlying database**. Only closing the odb file or saving it under a different name (File -> Save As) will save the database in the odb file.

___

## How to build the extension:

Normally, the extension is created with Eclipse for Java and [LOEclipse][32]. To work around Eclipse, I modified LOEclipse to allow the extension to be created with Apache Ant.  
To create the H2dbOOo extension with the help of Apache Ant, you need to:
- Install the [Java SDK][33] version 8 or higher.
- Install [Apache Ant][34] version 1.10.0 or higher.
- Install [LibreOffice and its SDK][35] version 7.x or higher.
- Clone the [H2dbOOo][36] repository on GitHub into a folder.
- From this folder, move to the directory: `source/H2dbOOo/`
- In this directory, edit the file: `build.properties` so that the `office.install.dir` and `sdk.dir` properties point to the folders where LibreOffice and its SDK were installed, respectively.
- Start the archive creation process using the command: `ant`
- You will find the generated archive in the subfolder: `dist/`

___

## Has been tested with:

* LibreOffice 24.2.1.2 (x86_64)- Windows 10

* LibreOffice 24.2.1.2 - Lubuntu 22.04

* LibreOffice 24.8.0.3 (x86_64) - Windows 10(x64) - Python version 3.9.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

I encourage you in case of problem :confused:  
to create an [issue][13]  
I will try to solve it :smile:

___

## Historical:

### What has been done for version 1.0.0:

- Implementation of a new format in odb files allowing the name of the catalog of the underlying database to be taken into account.

### What has been done for version 1.1.0:

- This version is based on [fix #154989][16] available since LibreOffice 24.2.x. It can therefore work with other extensions offering integrated database services.
- Now H2dbOOo requires LibreOffice 24.2.x minimum and will load for the url: `sdbc:embedded:h2`.

### What has been done for version 1.1.1:

- Updated the [Python packaging][37] package to version 24.1.
- Updated the [Python setuptools][38] package to version 72.1.0.
- The extension will ask you to install the jdbcDriverOOo extension in versions 1.4.2 minimum.

### What has been done for version 1.1.2:

- Fixed [issue #2][39] which appears to be a regression related to the release of JaybirdOOo. Thanks to TeddyBoomer for reporting it.
- Updated the [Python setuptools][38] package to version 73.0.1.
- Logging accessible in extension options now displays correctly on Windows.
- The extension options are now accessible via: **Tools -> Options... -> LibreOffice Base -> Embedded H2 Driver**
- Changes to extension options that require a restart of LibreOffice will result in a message being displayed.
- Support for LibreOffice version 24.8.x.

### What has been done for version 1.1.3:

- Requires the latest version of **jdbcDriverOOo 1.4.4**.
- In the extension options it is possible to define the options: **View system tables**, **Use bookmarks** and **Force SQL mode** which will be specific to this driver.

### What has been done for version 1.1.4:

- The extension will ask you to install jdbcDriverOOo extension in versions 1.4.6 minimum.
- Modification of the extension options accessible via: **Tools -> Options... -> LibreOffice Base -> Embedded H2 Driver** in order to comply with the new graphic charter.

### What has been done for version 1.2.0:

- Passive registration deployment that allows for much faster installation of extensions and differentiation of registered UNO services from those provided by a Java or Python implementation. This passive registration is provided by the [LOEclipse][32] extension via [PR#152][40] and [PR#157][41].
- Modified [LOEclipse][32] to support the new `rdb` file format produced by the `unoidl-write` compilation utility. `idl` files have been updated to support both available compilation tools: idlc and unoidl-write.
- It is now possible to build the oxt file of the H2dbOOo extension only with the help of Apache Ant and a copy of the GitHub repository. The [How to build the extension][42] section has been added to the documentation.
- Any errors occurring while loading the driver will be logged in the extension's log if logging has been previously enabled. This makes it easier to identify installation problems on Windows.
- Requires the **jdbcDriverOOo extension at least version 1.5.0**.

### What has been done for version 1.2.1:

- Many fixes that prevented proper functioning have been made to the driver written in Python and wrapping the driver that jdbcDriverOOo provides.
- Requires the **jdbcDriverOOo extension at least version 1.5.1**.

### What remains to be done for version 1.2.1:

- Add new language for internationalization...

- Anything welcome...

[1]: </img/h2db.svg#collapse>
[2]: <https://prrvchr.github.io/H2dbOOo/>
[3]: <https://prrvchr.github.io/H2dbOOo/README_fr>
[4]: <https://prrvchr.github.io/H2dbOOo/source/H2dbOOo/registration/TermsOfUse_en>
[5]: <https://prrvchr.github.io/H2dbOOo#what-has-been-done-for-version-121>
[6]: <https://prrvchr.github.io/>
[7]: <https://www.libreoffice.org/download/download/>
[8]: <https://www.openoffice.org/download/index.html>
[9]: <https://github.com/h2database/h2database>
[10]: <https://en.wikipedia.org/wiki/ACID>
[11]: <https://www.h2database.com/html/features.html#logging_recovery>
[12]: <https://github.com/prrvchr/H2dbOOo/>
[13]: <https://github.com/prrvchr/H2dbOOo/issues/new>
[14]: <https://prrvchr.github.io/jdbcDriverOOo/#requirement>
[15]: <https://bugs.documentfoundation.org/show_bug.cgi?id=156471>
[16]: <https://gerrit.libreoffice.org/c/core/+/154989>
[17]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[18]: <https://prrvchr.github.io/jdbcDriverOOo>
[19]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[20]: <https://img.shields.io/github/v/tag/prrvchr/jdbcDriverOOo?label=latest#right>
[21]: <img/H2dbOOo.svg#middle>
[22]: <https://github.com/prrvchr/H2dbOOo/releases/latest/download/H2dbOOo.oxt>
[23]: <https://img.shields.io/github/downloads/prrvchr/H2dbOOo/latest/total?label=v1.2.1#right>
[24]: <img/H2dbOOo-1.png>
[25]: <img/H2dbOOo-2.png>
[26]: <img/H2dbOOo-3.png>
[27]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/sdbc/Driver.html>
[28]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/sdbc/XConnection.html>
[29]: <https://github.com/prrvchr/H2dbOOo/blob/main/uno/lib/uno/embedded/documenthandler.py>
[30]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/util/XCloseListener.html>
[31]: <http://www.openoffice.org/api/docs/common/ref/com/sun/star/document/XStorageChangeListener.html>
[32]: <https://github.com/LibreOffice/loeclipse>
[33]: <https://adoptium.net/temurin/releases/?version=8&package=jdk>
[34]: <https://ant.apache.org/manual/install.html>
[35]: <https://downloadarchive.documentfoundation.org/libreoffice/old/7.6.7.2/>
[36]: <https://github.com/prrvchr/H2dbOOo.git>
[37]: <https://pypi.org/project/packaging/>
[38]: <https://pypi.org/project/setuptools/>
[39]: <https://github.com/prrvchr/HyperSQLOOo/issues/2>
[40]: <https://github.com/LibreOffice/loeclipse/pull/152>
[41]: <https://github.com/LibreOffice/loeclipse/pull/157>
[42]: <https://prrvchr.github.io/H2dbOOo/README_fr#comment-cr%C3%A9er-lextension>
