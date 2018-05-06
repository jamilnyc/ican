import datetime
import time

import s3


class NutrtritionReport:
    """
    Class responsible for generating the report file.

    Public Methods:
        getHTML()
    """
    s3Service = None

    def __init__(self):
        self.s3Service = s3.S3Service()

    def getReportName(self):
        """
        Return the path in S3 along with the file name containing the current date.

        :return: string file path and name
        """
        # string in the format 2018-05-31
        dateString = datetime.datetime.fromtimestamp(
            int(time.time())
        ).strftime('%Y-%m-%d')

        reportName = 'Nutrition_Report_' + dateString + '.html'
        fileName = 'reports/' + reportName
        return fileName

    def getHTML(self, nutrition):
        """
        Return URL to the HTML Nutrition Report.

        :param nutrition: A list of dictionaries with keys name, calories, total_fat, saturated_fat and sugar
        :return: Public S3 URL as a string
        """
        data = self.createHTMLPage(nutrition)
        fileName = self.getReportName()
        return self.s3Service.uploadData(data, fileName)

    def createHTMLPage(self, nutrition):
        """
        Return HTML file contents of the Nutrition report.

        :param nutrition: A list of dictionaries (see getHTML() function)
        :return: A string of formatted HTML code
        """
        html = '''
        <!doctype html>
        <html lang="en">
        <head>
            <title>iCan Nutrition Report</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
        </head>
        <body>
            <h1>Nutrition Report</h2> 
            <h2>Week of {0}</h2>
            {1}
            
            <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
        </body>
        </html>
        '''
        # Get the current week to print in the report as May, 31 2018
        week = datetime.datetime.fromtimestamp(
            int(time.time())
        ).strftime('%B %d, %Y')

        # Substitute values into the main HTML string
        tableHTML = self.getTableHTML(nutrition)
        formattedHTML = html.format(week, tableHTML)
        return formattedHTML
        
    def getTableHTML(self, nutrition):
        """
        Return HTML of the table that contains nutrition data.

        :param nutrition: nutrition: A list of dictionaries (see getHTML() function)
        :return: HTML code of the table as a string
        """
        html = '''
        <table class="table">
            <thead class="thead-dark">
                <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Calories</th>
                    <th scope="col">Total Fat (g)</th>
                    <th scope="col">Saturated Fat (g)</th>
                    <th scope="col">Sugar (g)</th>
                </tr>
            </thead>
        <tbody>
        '''
        for n in nutrition:
            # Highlight dangerous levels of sugar
            if n['sugar'] > 30:
                html += '<tr class="table-danger">'
            else:
                html += '<tr>'
                
            html += '<th scope="row">' + n['name'] + '</th>'
            html += '<td>' + str(n['calories']) + '</td>'
            html += '<td>' + str(n['total_fat']) + '</td>'
            html += '<td>' + str(n['saturated_fat']) + '</td>'
            html += '<td>' + str(n['sugar']) + '</td>'
            html += '</tr>'
            
        html += '</tbody></table>'
        return html
