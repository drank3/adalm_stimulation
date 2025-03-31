import pyvisa
import matplotlib.pyplot as plt
import numpy as np


#This is the first of four files for Keithley operation, covering basic functions for pulsing
class Keithley_Runtime:
    #TODO: Reformat all single-line Serial commands to multi-line

    """
    This function initialized the Keithley based on a specified resource channel ('COM3', 'COM4', etc.)
    The baud rate is set by default to 115200, but must also be configured as such on the Keithley hardware menu"
    """
    def initialize_keithley(self, resource_name, baud_rate=115200):
        """Initialize the Keithley device"""
        rm = pyvisa.ResourceManager()
        instrument = rm.open_resource(resource_name,
                                      baud_rate=baud_rate,
                                      )
        instrument.timeout = 500000  # Set timeout in milliseconds

        # Reset and clear the unit
        instrument.write("*RST")
        instrument.write("*CLS")

        print(f"Connected to: {instrument.query('*IDN?').strip()}")
        return instrument


    def Configure_Voltage_Pulse(self, instrument, pulse_voltage, pulse_width, bias_voltage, pulse_nos, freq, pulse_train_id):

        p_off = 1/freq - pulse_width
        instrument.write("smub.reset()")
        instrument.write("smub.source.rangev = 5")
        instrument.write("smub.source.rangei = 1")
        instrument.write("smub.source.levelv = 0")
        instrument.write("smub.measure.rangev = 5")
        instrument.write("smub.measure.rangei = 1")
        instrument.write("smub.measure.nplc = 0.01")
        instrument.write("smub.measure.autozero = smub.AUTOZERO_ONCE")
        instrument.write("smub.nvbuffer1.clear()")
        instrument.write("smub.nvbuffer1.appendmode = 1")

        instrument.write(f"f1, msg1 = ConfigPulseVMeasureI(smub, 0, {pulse_voltage}, 1, {pulse_width}, {p_off}, {pulse_nos}, smub.nvbuffer1, {pulse_train_id})")
        instrument.write("f2, msg2 = InitiatePulseTest(1)")
        results = instrument.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1)")

        return results

    def Configure_Current_Pulse(self, instrument, pulse_current, pulse_width, bias_current, pulse_nos, freq, pulse_train_id,
                                meas_interval=.001):

        p_off = 1 / freq - pulse_width

        pulse_points = pulse_width/meas_interval
        interval_points = p_off/meas_interval

        instrument.write("smub.reset()")
        instrument.write("smub.source.rangev = 10")
        instrument.write("smub.source.rangei = 1")
        instrument.write("smub.measure.nplc = 0.01")
        instrument.write("smub.measure.rangev = 10")
        instrument.write("smub.measure.rangei = 1")
        instrument.write("smub.measure.autozero = smub.AUTOZERO_ONCE")
        instrument.write("smub.trigger.measure.action = smub.ASYNC")
        instrument.write("smub.nvbuffer1.clear()")
        instrument.write("""
        smub.nvbuffer1.appendmode=1
        smub.nvbuffer2.clear()""")
        instrument.write("smub.nvbuffer2.appendmode=1")
        instrument.write("smub.nvbuffer1.collectsourcevalues = 0")
        instrument.write("smub.nvbuffer2.collectsourcevalues = 0")




        instrument.write("smub.source.output = smub.OUTPUT_ON")



        instrument.write(f"f1, msg1 = ConfigPulseIMeasureV(smub, {bias_current}, {pulse_current}, 10, {pulse_width}, {p_off}, {pulse_nos}, smub.nvbuffer1, {pulse_train_id})")
        return 10



    def Initiate_Pulse_Test(self, instrument, test_no):
        #instrument.write("smub.measure.overlappedi(smub.nvbuffer1)")

        instrument.write(f"f2, msg2 = InitiatePulseTest({test_no})")


        results_i = np.fromstring(instrument.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)"), sep=",")

        #return np.array([1])
        return results_i

    def Initiate_Linear_Voltage_Sweep(instrument, start_voltage, end_voltage, step, settling_time):
        point_no = abs(end_voltage-start_voltage)/step
        instrument.write("smub.reset()")
        instrument.write("smub.nvbuffer1.clear()")
        instrument.write(f"SweepVLinMeasureI(smub, {start_voltage}, {end_voltage}, {settling_time}, {point_no})");
        return instrument.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)")





    def reset_SMU_buffers(self, instrument):
        instrument.write("smub.nvbuffer1.clear()")
        instrument.write("smub.nvbuffer2.clear()")
        instrument.write("smua.nvbuffer1.clear()")
        instrument.write("smua.nvbuffer2.clear()")

    def close_connection(self, instrument):
        """Close the connection to the Keithley device."""
        instrument.write(f"smub.source.output = smub.OUTPUT_OFF")
        instrument.close()
        print("Connection closed")

    def multi_line_test(self, instrument):
        pass


# Main script
if __name__ == "__main__":
    try:

        resource_name = "COM5"
        krt = Keithley_Runtime()
        keithley = krt.initialize_keithley(resource_name)


        Configure_Current_Pulse(keithley, .001, .001, 0, 10, 500, 1)
        results = krt.Initiate_Pulse_Test(keithley, 1)





    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close connection
        close_connection(keithley)
        print("Done")
