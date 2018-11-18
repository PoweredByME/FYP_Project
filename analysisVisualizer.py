'''
    This script uses matplotlib's pyplot that is why
    it is not the child of a worker. It is instantiated 
    in the server and displays the content is a serial
    manner.
'''
from matplotlib import pyplot as plt;
from matplotlib import animation;
class analysisVisualizer(object):
    '''
        This class has custom function and for adding new 
        grahps and views make new custom functions.
    '''
    def _addSubPlot(self ,plot_dict, rows, cols, plot_idx):
        plot_dict["subplot" + str(rows) + str(cols) + str(plot_idx)] = plot_dict["fig"].add_subplot(rows, cols, plot_idx);

    def __init__(self):
        self._fft_plot_for_4_channel_data = {'fig' : plt.figure()};
        self._fft_plot_for_4_channel_data['data'] = None
        for i in range(1,5):
            self._addSubPlot(self._fft_plot_for_4_channel_data, 4, 1, i)
        

    def show(self):
        plt.ion();
        plt.show();

    def SET_DATA__fft_plot_for_4_channel_data(self, data):
        self._fft_plot_for_4_channel_data["data"] = data
        self._animate_fft_plot_for_4_channel_data();

    def _animate_fft_plot_for_4_channel_data(self):
        data = self._fft_plot_for_4_channel_data["data"];
        fig = self._fft_plot_for_4_channel_data["fig"];
        _i = 1;
        if data is None:
            return;
        for _item in data:
            
            xs = [_item["fAx"][13], _item["fAx"][15]];
            ys = [_item["fftData"][13], _item["fftData"][15]];
            self._fft_plot_for_4_channel_data["subplot41" + str(_i)].clear();
            self._fft_plot_for_4_channel_data["subplot41" + str(_i)].stem(ys);
            _i += 1;

        plt.draw();
        plt.pause(0.000001);

        
        

a = analysisVisualizer();
