#include <LPC17xx.h>
#include <stdio.h>
#define Ref_Vtg 5.000
#define Full_Scale 0xFFF

extern unsigned long int temp1, temp2;

unsigned long int temp1 = 0, temp2 = 0;
#define RS_CTRL 0x00000100
#define EN_CTRL 0x00000200
#define DT_CTRL 0x00000FF0

void lcd_init(void);
void wr_cn(void);
void clr_disp(void);
void delay_lcd(unsigned int);
void lcd_com(void);
void wr_dn(void);
void lcd_data(void);
void clear_ports(void);
void lcd_puts(char *);


int main(void)
{
    unsigned int adc_temp;
    unsigned int i, sample_count = 10;
    float in_vtg;
    float moisture_avg = 0;
    float moisture_percentage_value = 0;
    char vtg[14], dval[14], moisture_percentage[14];
    char status[10];  // To store the status message: LOW, OK, or HIGH
    SystemInit();
    SystemCoreClockUpdate();
    lcd_init();
    
    LPC_PINCON->PINSEL1 |= 1 << 14; // Configuring Pin P0.23 for ADC functionality
    LPC_GPIO1->FIODIR = 0xFFFFFFFF;
	
    LPC_SC->PCONP |= (1 << 12);     // Powering up the ADC

    temp1 = 0x80;
    lcd_com();
    delay_lcd(80000);
    lcd_puts("Moisture in soil:");

    while (1)
    {
        moisture_avg = 0;

        // Take multiple ADC samples for averaging
        for (i = 0; i < sample_count; i++)
        {
            LPC_ADC->ADCR = (1 << 0) | (1 << 21) | (1 << 24); // Start ADC conversion

            while (((adc_temp = LPC_ADC->ADGDR) & 0X80000000) == 0); // Wait for conversion
            adc_temp = LPC_ADC->ADGDR; 
            adc_temp = (adc_temp >> 4) & 0xFFF; // Mask upper bits to get a 12-bit result
            
            moisture_avg += adc_temp; // Accumulate the readings
            delay_lcd(1000); // Short delay between readings
        }
        
        // Calculate the average ADC reading
        moisture_avg /= sample_count;
        
        // Convert to percentage
        moisture_percentage_value = (1 - (moisture_avg / Full_Scale)) * 100.0;

        // Determine the status based on the moisture percentage
        if (moisture_percentage_value < 35.0) {
						sprintf(moisture_percentage, "%0.1f%% (LOW)", moisture_percentage_value);
            sprintf(status, "LOW ");
						LPC_GPIO1->FIOPIN= 0xFFFFFFFF;
						for(i = 0; i < 800000; i++);
						LPC_GPIO1->FIOPIN= 0;
					} else if (moisture_percentage_value > 80.0) {
            sprintf(moisture_percentage, "%0.1f%% (HIGH)", moisture_percentage_value);
						LPC_GPIO1->FIOPIN= 0xFFFFFFFF;
            sprintf(status, "HIGH");
        } else {
						sprintf(moisture_percentage, "%0.1f%% (OK)", moisture_percentage_value);
            
						LPC_GPIO1->FIOPIN= 0x0;
            sprintf(status, "OK  ");
        }

        // Display the percentage value
        temp1 = 0xC0;
        lcd_com();
        delay_lcd(50000);
        lcd_puts(moisture_percentage);

        // Display the status message
        temp1 = 0x94; // Move to a new line on the LCD for the status message
        lcd_com();
        delay_lcd(50000);
        lcd_puts("Status: ");
        lcd_puts(status);

        delay_lcd(500000); // Delay before the next reading
				
        for(i = 0; i < 2000000; i++);
    }
}



void lcd_init()
{

    LPC_PINCON->PINSEL0 &= 0X00000000; // Configuring pins as
    LPC_GPIO0->FIODIR |= DT_CTRL;      // Configuring data pins as output
    LPC_GPIO0->FIODIR |= RS_CTRL;      // Configuring RS pin as output
    LPC_GPIO0->FIODIR |= EN_CTRL;      // Configuring EN pin as output
    clear_ports();
    delay_lcd(3200); // Power-on delay

    temp2 = (0x30);
    wr_cn();
    delay_lcd(30000);
    temp2 = (0x30);
    wr_cn();
    delay_lcd(30000);

    temp2 = 0x30;
    wr_cn();
    delay_lcd(30000);

    temp2 = (0x20);
    wr_cn();
    delay_lcd(30000);

    temp1 = 0x28;
    lcd_com();
    delay_lcd(30000);

    temp1 = 0x0c;
    lcd_com();
    delay_lcd(800);

    temp1 = 0x06;
    lcd_com();
    delay_lcd(800);

    temp1 = 0x01;
    lcd_com();
    delay_lcd(10000);

    temp1 = 0x80;
    lcd_com();
    delay_lcd(800);
    return;
}

void lcd_com(void)
{
    temp2 = temp1 & 0xf0;
    temp2 = temp2;
    wr_cn();
    temp2 = temp1 & 0x0f;
    temp2 = temp2 << 4;
    wr_cn();
    delay_lcd(1000);
    return;
}

void wr_cn(void)
{
    clear_ports();
    LPC_GPIO0->FIOPIN = temp2;
    LPC_GPIO0->FIOCLR = RS_CTRL;
    LPC_GPIO0->FIOSET = EN_CTRL;
    delay_lcd(25);
    LPC_GPIO0->FIOCLR = EN_CTRL;
    return;
}

void lcd_data(void)
{
    temp2 = temp1 & 0xf0;
    temp2 = temp2;
    wr_dn();
    temp2 = temp1 & 0x0f;
    temp2 = temp2 << 4;
    wr_dn();
    delay_lcd(1000);
    return;
}

void wr_dn(void)
{
    clear_ports();
    LPC_GPIO0->FIOPIN = temp2;
    LPC_GPIO0->FIOSET = RS_CTRL;
    LPC_GPIO0->FIOSET = EN_CTRL;
    delay_lcd(25);
    LPC_GPIO0->FIOCLR = EN_CTRL;
    return;
}

void delay_lcd(unsigned int r1)
{
    unsigned int r;
    for (r = 0; r < r1; r++)
        ;
    return;
}
void clr_disp(void)
{
    temp1 = 0x01;
    lcd_com();
    delay_lcd(10000);
    return;
}

void clear_ports(void)
{
    LPC_GPIO0->FIOCLR = DT_CTRL;
    LPC_GPIO0->FIOCLR = RS_CTRL;
    LPC_GPIO0->FIOCLR = EN_CTRL;
    return;
}

void lcd_puts(char *buf1)
{
    unsigned int i = 0;

    while (buf1[i] != '\0')
    {
        temp1 = buf1[i];
        lcd_data();
        i++;

        if (i == 27)
        {
            temp1 = 0xc0;
            lcd_com();
        }
    }
    return;
}


