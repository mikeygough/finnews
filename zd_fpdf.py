from fpdf import FPDF
import numpy as np


class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L')
        self.add_page()
        self.set_margin(0)


    def draw_circle(self, xpos, ypos, rad=25, symbol='', name=''):
        '''
        draws a filled in circle of radius rad as xpos, ypos
        xpos: abscissa of upper-left bounding box
        ypos: ordinate of upper-left bounding box
        rad: radius of circle, default 25
        symbol: product symbol
        name: product name
        '''
        self.set_line_width(1)
        self.set_draw_color(240)
        self.set_fill_color(r=83, g=167, b=219)
        self.circle(x=xpos, y=ypos, r=rad, style='F')

        # add text annotation
        self.set_font('Arial', 'B', 16)
        self.set_xy(xpos, ypos)
        self.cell(w=rad, h=rad-2, txt='{}'.format(symbol), align='C')

        self.set_font('Arial', '', 14)
        self.set_xy(xpos, ypos*2.85)
        self.cell(w=rad, h=rad-2, txt='{}'.format(name), align='C')


    def draw_hilo(self, high, low, close,
              x_start, y_start,
              x_end, y_end):
        '''
        draws a high-low-close line with circle at the current price
        high: underlying high price
        low: underlying low price
        x_start: abscissa of first point
        y_start: ordinate of first point
        x_end: abscissa of second point
        y_end: ordinate of second point
        '''
        # draw line
        self.set_line_width(1)
        self.set_draw_color(r=112, g=112, b=112)
        self.line(x1=x_start, y1=y_start,
                 x2=x_end, y2=y_end)

        # calculate line length
        length = np.sqrt((x_end - x_start) ** 2 + (y_end - y_start) ** 2)
        # calculate position percent
        close_pct = close / high
        # calculate additional line pos
        additional_pos = close_pct * length
        # calculate circle position
        circle_x_position = additional_pos + x_start

        # draw circle at position
        self.draw_circle(xpos=circle_x_position, ypos=y_start-1.5, rad=3)

        # add annotations
        self.set_font('Arial', '', 12)
        
        # draw low text
        self.set_xy(x_start - self.get_string_width('{}'.format(low)) - 2,
                   y_start-8)
        self.cell(h=10, txt='{:.2f}'.format(low), align='L')
        self.set_xy(x_start - self.get_string_width('Low') - 2, y_start-2)
        self.cell(h=10, txt='Low', align='L')

        # draw high text
        self.set_xy(x_end, y_end-8)
        self.cell(h=10, txt='{:.2f}'.format(high), align='L')
        self.set_xy(x_end, y_end-2)
        self.cell(h=10, txt='High', align='L')
        
        # draw close text
        self.set_font('Arial', '', 14)
        self.set_xy(circle_x_position - (self.get_string_width('{}'.format(close)) / 2),       y_end-12)
        self.cell(h=10, txt='{:.2f}'.format(close), align='C')


    def draw_sd(self, xpos, ypos, sd):
        '''
        draws a normal distribution with 1, 2 & 3 sd movement values
        xpos: x position
        ypos: y position
        sd: float standard deviation.
        '''

        # standard curve
        self.image('static/distribution.png', x=xpos, y=ypos,
                  h=30, w=100)

        # add annotations
        self.set_font('Arial', '', 12)
        
        # draw low text
        sd_one_len = self.get_string_width(str(int(sd)))
        sd_two_len = self.get_string_width(str(int(sd * 2.0)))
        sd_three_len = self.get_string_width(str(int(sd * 3.0)))
        
        # low 3
        self.set_xy(xpos*1.05, ypos+28)
        self.cell(h=10, txt='{}'.format(int(sd * 3.0)), align='L')

        # low 2
        self.set_xy(xpos*1.19, ypos+28)
        self.cell(h=10, txt='{}'.format(int(sd * 2.0)), align='L')

        # low 1
        self.set_xy(xpos*1.35, ypos+28)
        self.cell(h=10, txt='{}'.format(int(sd)), align='L')

        # high 1
        self.set_xy(xpos*1.53, ypos+28)
        self.cell(h=10, txt='{}'.format(int(sd)), align='L')

        # high 2
        self.set_xy(xpos*1.66, ypos+28)
        self.cell(h=10, txt='{}'.format(int(sd * 2.0)), align='L')

        # high 3
        self.set_xy(xpos*1.80, ypos+28)
        self.cell(h=10, txt='{}'.format(int(sd * 3.0)), align='L')


def main():
    # create pdf
    pdf = PDF()
    # describe pdf
    print("page layout", pdf.page_layout)
    # unit mm
    print("default page dimensions", pdf.default_page_dimensions)
    # (841.89, 595.28)mm
    
    # draw sd
    pdf.draw_sd(xpos=105, ypos=7, sd=25)

    # symbol circle
    pdf.draw_circle(xpos=10, ypos=10, symbol='/ES')

    # high low close
    pdf.draw_hilo(high=100, low=10, close=79, 
              x_start=55, y_start=22,
              x_end=100, y_end=22)

    # sample chart
    pdf.image('static/chart.png', x=190, y=8,
    h=30, w=100)

    # output file
    pdf.output('static/test-fpdf.pdf')


if __name__ == '__main__':
    main()
