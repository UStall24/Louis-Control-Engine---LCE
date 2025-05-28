using System.Windows;
using UStallGUI.Model;
using UStallGUI.ViewModel;

namespace UStallGUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            // Main Prog Entry Point
            ConfigLoader.CurrentConfig = ConfigLoader.LoadConfigGUI();
            InitializeComponent();
            DataContext = new MainWindowViewModel();
        }
    }
}