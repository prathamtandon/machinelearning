import matplotlib.pyplot as plt
from constants import instance_scale

def plot_mistakes (p_mistakes_no_margin, p_mistakes_margin, w_mistakes_no_margin, w_mistakes_margin):
    plt.plot(instance_scale, p_mistakes_no_margin, 'r-', label='perceptron without margin')
    plt.plot(instance_scale, p_mistakes_margin, 'b--', label='perceptron with margin')
    plt.plot(instance_scale, w_mistakes_no_margin, 'g-.', label='winnow without margin')
    plt.plot(instance_scale, w_mistakes_margin, 'y:', label='winnow with margin')
    plt.legend(loc='upper left')
    plt.savefig('plot2.pdf')

def plot_learning_curves (yvalues, xvalues, filename, label):
    print str(xvalues)
    print str(yvalues)
    plt.plot(xvalues, yvalues, label=label)
    plt.legend(loc='upper left')
    plt.savefig(filename + '.pdf')
