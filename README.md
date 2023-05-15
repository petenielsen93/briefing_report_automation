# briefing_report_automation

Hello!

This project is an automated data cleaning and reporting tool for Inteserra Inc's Briefing Services, which is a breaking news service that details regulatory developments in the telecommunications industry. The tool generates a report outlining the companies that view/download our product, down to who within that company and which briefings they were viewing specifically. This allows us to know which developments garner more attention than others, who uses the product faithfully enough to gather feedback from, and which companies are finding our product useful. 

The original tool takes a csv of our user data (sample data provided in Data folder) downloaded from our product's backend, cleans it using Python, and displays it on a word document template for easy readability by members of our consulting staff (who aren't very tech friendly). 

The tool as of May 15 opens a tkinter GUI, which allows any consultant member to select any Excel or csv file from our product's backend for importing. Using Python, the script cleans the data and then generates an updated Microsoft Word template and a PDF version of the report into your Downloads folder using docxtpl's DocXTemplate and docx2pdf converter. The report now includes a pie chart of one of the most important metrics, which was built using Python's matplotlib library.
