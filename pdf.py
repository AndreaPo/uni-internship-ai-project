import fpdf

class Pdf(fpdf.FPDF):
    def header(self):
        #set the font, bold, font-size
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(30,10,"Esercise",border=0,ln=0)
        self.ln(20)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0,10, 'Page' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    