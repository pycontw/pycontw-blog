Title: PyCon APAC 自造RFID讀卡機，快速完成會議報到系統
Date: 2015-06-01 22:46:00
Category: programs
Tags: legacy-blogger
Slug: 2015-06-01-pycon-apac-rfid
Authors: PyCon Taiwan Blogger contributors

*This was originally posted on blogger [here](https://pycontw.blogspot.com/2015/06/pycon-apac-rfid.html)*.

<!--more-->

最近只要聽到自造者(Self-Maker)，許多人的眼睛就亮了！可以寫變出機器人、家用電視盒，接上感測器可以馬上偵測周遭環境而做出應對，這種能力讓自造者越來越火紅。也讓許多沒有經驗的人躍躍欲試，希望自己能來上一手。

亞太區最大的 Python 年會 ── PyCon APAC 2015 就是用知名的 Raspberry Pi 快速設計報名系統的解決方案。這套方案的催生，是透過社群自主舉辦的 Workshop 活動，搭配快速上手的 Python 語言，在短時間催生出一套穩定可用的系統。這同時也是 Raspberry Pi + Python 吸引人的地方－你可以在短時間兜建出一套 Prototype 設備，滿足你對軟硬整合實作的無限想像。

在此之前，研討會本身的註冊與報到一直是相當棘手的事情。催生這套系統的樹莓派講師 Sosorry 表示：『在過去，都是以人工識別參加者的身份並換發識別證，耗時又費工。據統計，平均報名人數每多 100 人就需要多開一個報到櫃台來處理，舉例來說，台灣最大開源活動 COSCUP ，在2012 年就開了 10 個櫃台服務約 1,100 人的報到流程。像這麼大的工作量，若只靠人，一定會出錯！』依照過往的經驗，每分鐘約可處理11人的報到量。

『2013 與 2014 年的 COSCUP，使用近場通訊技術(NFC)，可以達到每 1.46 秒完成一個人的報到程序，也就是每分鐘處理 41 人的報到量，整整是人工處理的 3 倍多！』可見使用這樣的系統之後，報名速度提昇不少。最酷的是，這完全是可以一個人獨立完成的事情！

![](https://lh6.googleusercontent.com/O3SaVRFouillhzZwxI4B2Q4AsJwtBRhmervLIz5QGQiHMf6pwVLGrWDZPvVIFNiDUGOyW99OhNJm5FlV1yvUpCPSZgxSOSRzxS9myo-Qok-pDwebOriOjj7PMEYEHGAGKocm2XQ)

版權屬於：COSCUP 2013，來源：https://www.flickr.com/photos/coscup/9634483039/

今年面對 PyCon APAC 2015超過700 人的參與人數。在票券選擇上使用了 RFID，搭配頻率相同的 NFC 讀取機，預計可加速報到流程。尤其這個技術目前已經相當成熟。單張 RFID 卡片價格低廉，而一台以 Raspberry Pi 全自造的 NFC 讀取機成本只在台幣 5000 塊左右。這樣的解決方案最適合財務來源匱乏的自發式社群。Sosorry也提到，『除此之外，這套系統將帶出與會者的所有資訊，屆時不只是報到，連便當、衣服領取、參加的活動，都將更方便。』 贊助組組長 David 補充，『而想投履歷到各家參展公司的人，也只需要感應你手上的卡片即可，相當方便！』

![PyConAPAC.jpg](https://lh5.googleusercontent.com/USbs7vB3-4uxo1g2hSTGfzI2AYVQZ5FzazYn6PGp9uNINxmRiBkN9JCiimY6MsgPKDb_IsjtQkQtBdg7VCVD4LiL6eMohxjpthMebhgZQ4Xd_LT582Pj094zcQ6N7gjJB-8cNqQ)

版權屬於：Sosorry, PyCon APAC 2015

Raspberry Pi (樹莓派) 是對於自造者而言最簡單的入門系統，小小一塊基板卻包含大部分硬體開發的設備需求，從處理器到 GPIO 接腳，從支持 wifi 到各式感應器，提供想學習硬體的初學者一個相當漂亮的入門磚。除了設備完整之外，Raspberry Pi 還支援近來相當火紅的語言 - Python 撰寫。也降低了許多人對硬體操作的門檻。

今年由台灣 Python 年會組織委員會主辦，在中央研究院的大型 PyCon APAC 2015 亞太區 Python 年會，預計將吸引超過 700 位國內外軟體工程師齊聚一堂，以『Back to \_\_future\_\_ ||』 為主題，提供參與者一同研究新未來。
