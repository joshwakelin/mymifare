<!-- PROJECT LOGO -->
<br />


  # MyMifare


   <h4>An open sourced, byte manipulation tool for Mifare NFC cards.</h4>
 
   
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

MyMifare is a versatile, easy-to-use byte manipulation software designed to seamlessly read, write, save, and edit Mifare card data. Lightweight by design, MyMifare runs directly from a terminal, making it a easy solution for developers, hobbyists, and professionals looking for a basic tool without unnecessary overhead.

With its intuitive command-line interface, MyMifare offers precise control over Mifare card sectors, blocks, and bytes, empowering users to manipulate data efficiently. The software supports common Mifare card operations, including key management, sector authentication, and backup creation, ensuring reliability and ease of use for a variety of applications.

Whether you're working in security, access control, public transit systems, or simply exploring RFID technology, MyMifare delivers the tools you need in a compact and efficient package.


### Built With

* [Python](https://www.python.org/)
* [Pyscard](https://pyscard.sourceforge.io/)


<!-- GETTING STARTED -->
## Getting Started

### Software Prerequisites

MyMifare requires Python and the necessary libraries to function correctly. To install the required dependencies, simply run the following command in a terminal in the root folder:

* pip
  ```sh
  pip install -r requirements.txt
  ```

 This command will install all the necessary Python packages listed in the requirements.txt file, which is required for proper operation.

### Hardware Requirements
In addition to the software dependencies, MyMifare requires an NFC card reader to interact with Mifare cards. The software is compatible with a variety of NFC card readers, and was persoanlly tested using an **ACR122U.**

### Start-up

Startup is easy. After installing to the dependanies, run the following command in a terminal in the root folder
* pip
  ```sh
  startup
  ```

  After startup is completed, MyMifare will attempt to establish a connection with a USB card reader, plugged into your PC or Laptop. Note, this has **3** attempts, before the program force closes. It's recommended you have your USB card reader and Mifare card on the reader prior to program startup. 


<!-- USAGE EXAMPLES -->
## Usage
After the program has had dependancies installed and startup is completed, the main menu should appear, as depicted below.

Each menu item cooresponds to a 




<!-- ROADMAP -->
## Features

- [x] 
- [ ]



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


