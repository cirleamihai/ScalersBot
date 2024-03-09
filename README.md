## DEVELOPMENT AND DISTRIBUTION OF THIS BOT IS ROOTED IN EDUCATIONAL PURPOSES ONLY. USING IT FOR COMMERCIAL INTERESTS IS STRICTLY FORBIDDEN.

# ScalersBot (2021 - 2022, endpoints could be deprecated)

This project comprises a sophisticated bot system designed to automate monitoring and interaction with Sizeer's both frontend and backend. It includes functionality for **web scraping their WebAPP and MobileAPP**, **product monitoring**, **special accounts generation**, and **automated purchasing**. Optimized for the 2021-2022 sneaker market dynamics, it is calibrated for making instant value assessments, distinguishing between worthwhile investments and less desirable options.

**IMPORTANT MENTION**: The checkout flow is an advanced and well engineered module that can handle unexpected errors and make dynamic decisions based on given set of rules. It is designed to be able to **start, stop and update itself according to different website changes and anti-bots challenges(by complying to the website's TOS).** You can call it an autonomous bot.

It is connecting two important parts: Product Monitoring with latencies close to 1 ~ 2 seconds for real-time changes and the checkout module, ready to complete the purchase in unbelievably fast times, leaving 0 chances for manual users.

## Features

- **Multi-threading support** for efficient task handling on Sizeer and Supreme.
- **Tool functions** for:
    - handling _Products, Accounts and Websites Databases_ (JSON, CSV, TXT)
    - creating _custom requests clients_ (mimicking real browsers)
    - gaining _total anonymity by using large pools of User-Agents, Residential and Datacenter Proxies_
    - large amounts of _data prelucration and validation_
    - checking for _corrupted storage_
    - randomizing _email, password and shipping information_

- **Custom Requests Client** which performs a :
    - **TLS Handshake**:
       - mimicks the handshake process by generating and exchanging **keys**, **cipher suites**, **TLS versions**, and possibly **session tickets** (if resuming a session)
    - **Certificate Verification**
    - **Encryption Setup**
    - and establishes a **Secure Communication Channel**: The data is encrypted using the session keys to maintain confidentiality and integrity.
    - **more details in TLS/tlsclient.py**

- **Monitoring Modules**:
    - performs a real time product scanning on different endpoints for
      - Sizeer Romania (sizeer.ro)
      - Sizeer Germany (sizeer.de)
      - Sizeer Poland (sklep.sizeer.com)
      - Supreme (supreme.eu)
    - have the option to intialize checkout tasks for new products
- **Checkout Modules**:
  - Sizeer (.ro, .de):
    - Guest Mode (5 - 6 seconds checkout time)
    - Account Mode (10 seconds checkout time):
      - Connects their Mobile App and their WebAPP by issuing concurrent and iterative requests
      - Used for special products
    - Preload mode (2 - 3 seconds checkout time)
    - AUTO MODE (integrated with the Monitoring Module)
  - Supreme (not working, deprecated)
- **Uses environment variables for secure data handling.**
- **Account generator tool**:
  - **Sizeer Mobile**:
     - Creates mobile accounts with bonus points attached
- **Discord Integration**
  - **Instant Notifications**: Utilizes Discord webhooks for real-time alerts on product launches, stock changes, and checkout statuses, keeping the user informed in real time.
  - **Detailed Product Alerts**: Provides comprehensive product details including direct add-to-cart links, price, and size availability through Discord notifications.
- **User-Friendly Utilities**
  - **Keyword Filtering**: Employs a sophisticated filtering system to monitor specific products based on user-defined keywords, enhancing targeting precision
    
## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-github-username/your-repo-name.git
cd your-repo-name
```
2. **Install dependencies**

Ensure you have Python 3.7 or higher installed on your system. Then install the required dependencies:

```bash
pip install -r requirements.txt
```
3. **Run the bot**
```bash
python ScalersBot.py
python .\Modules\Sizeer\Monitors\RO\dunks_monitor.py
python .\Modules\Sizeer\Monitors\RO\jordan_monitor.py
... similar for other monitors
```

## IMPORTANT NOTES

While the development and distribution of ScalersBot is rooted in educational purposes, showcasing the capabilities and intricacies involved in creating sophisticated automation tools, it is **crucial** to emphasize the **ethical considerations** and **legal boundaries** surrounding its usage.

### **Educational Use Only**

- This project is designed **strictly for educational and research purposes**. It serves as a practical example to understand web automation, network requests, data parsing, and the application of TLS within custom clients.
- Users are encouraged to explore the codebase to gain insights into the technical aspects of bot development and to learn about the challenges and solutions in automating web interactions.

### **Strictly Discourage Illegal Use**

- The creator of ScalersBot **strongly discourages and disclaims any liability** for the use of this software in violating the terms of service or terms of use of any website, including Sizeer and Supreme.
- Users must **respect the terms of service** of any platform they interact with. Unauthorized use of automation tools can lead to legal consequences and violate the ethical standards of the software development community.

### **No Liability**

- By using ScalersBot, you acknowledge that you are doing so at **your own risk**. The creator **will not be held responsible** for any actions taken with this tool, including any form of misuse or activities deemed illegal by governing laws or website policies.
- The responsibility lies solely with the user to ensure their actions are **legal**, **ethical**, and **in compliance** with all applicable rules and regulations.

### **Contribute Ethically**

- Contributors are welcome to improve the project, but must also ensure that their contributions **do not promote or facilitate unethical or illegal activities**. Enhancements should focus on the educational value and technical advancements in a manner that respects legal boundaries.

In summary, ScalersBot is a tool meant to inspire and educate, providing a hands-on approach to learning about software automation and network communications. It is imperative that its use remains within the scope of learning, experimentation, and research within ethical and legal frameworks.
