using System.Diagnostics;
using System.Drawing;
using System.Windows.Forms;

namespace OffTimer;

internal static class Program
{
    [STAThread]
    static void Main()
    {
        ApplicationConfiguration.Initialize();
        Application.Run(new MainForm());
    }
}

public sealed class MainForm : Form
{
    private DateTime? shutdownAt;
    private readonly Label timeLabel;
    private readonly Label statusLabel;
    private readonly System.Windows.Forms.Timer timer;

    public MainForm()
    {
        Text = "OffTimer";
        ClientSize = new Size(400, 285);
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        StartPosition = FormStartPosition.CenterScreen;
        Font = new Font("Malgun Gothic", 9F);

        Controls.Add(new Label {
            Text = "OffTimer",
            Font = new Font("Malgun Gothic", 18F, FontStyle.Bold),
            AutoSize = true,
            Location = new Point(145, 22)
        });

        Controls.Add(new Label {
            Text = "남은 시간",
            AutoSize = true,
            Location = new Point(171, 65)
        });

        timeLabel = new Label {
            Text = "00:00:00",
            Font = new Font("Consolas", 30F, FontStyle.Bold),
            TextAlign = ContentAlignment.MiddleCenter,
            Size = new Size(360, 58),
            Location = new Point(20, 80)
        };
        Controls.Add(timeLabel);

        var tenMin = new Button {
            Text = "+ 10분", Size = new Size(130, 45), Location = new Point(65, 145)
        };
        tenMin.Click += (_, _) => ScheduleShutdown(TimeSpan.FromMinutes(10));
        Controls.Add(tenMin);

        var oneHour = new Button {
            Text = "+ 1시간", Size = new Size(130, 45), Location = new Point(205, 145)
        };
        oneHour.Click += (_, _) => ScheduleShutdown(TimeSpan.FromHours(1));
        Controls.Add(oneHour);

        var cancel = new Button {
            Text = "예약 취소", Size = new Size(130, 34), Location = new Point(65, 198)
        };
        cancel.Click += (_, _) => CancelShutdown();
        Controls.Add(cancel);

        var now = new Button {
            Text = "지금 종료", Size = new Size(130, 34), Location = new Point(205, 198)
        };
        now.Click += (_, _) => ShutdownNow();
        Controls.Add(now);

        statusLabel = new Label {
            Text = "예약된 종료 없음",
            TextAlign = ContentAlignment.MiddleCenter,
            Size = new Size(360, 30),
            Location = new Point(20, 240)
        };
        Controls.Add(statusLabel);

        timer = new System.Windows.Forms.Timer { Interval = 500 };
        timer.Tick += (_, _) => UpdateDisplay();
        timer.Start();

        FormClosing += (_, _) => {
            RunShutdown("/a");
            shutdownAt = null;
        };

        UpdateDisplay();
    }

    private void ScheduleShutdown(TimeSpan addition)
    {
        var now = DateTime.Now;
        var remaining = shutdownAt.HasValue && shutdownAt.Value > now
            ? shutdownAt.Value - now
            : TimeSpan.Zero;

        var total = remaining + addition;
        var seconds = Math.Max(1, (int)Math.Ceiling(total.TotalSeconds));
        shutdownAt = now.AddSeconds(seconds);

        RunShutdown("/a");
        RunShutdown($"/s /t {seconds}");
        UpdateDisplay();
    }

    private void CancelShutdown()
    {
        RunShutdown("/a");
        shutdownAt = null;
        UpdateDisplay();
    }

    private void ShutdownNow()
    {
        if (MessageBox.Show(
            "정말 지금 컴퓨터를 종료하시겠습니까?",
            "시스템 종료",
            MessageBoxButtons.YesNo,
            MessageBoxIcon.Warning) == DialogResult.Yes)
        {
            RunShutdown("/s /t 0");
        }
    }

    private void UpdateDisplay()
    {
        if (!shutdownAt.HasValue)
        {
            timeLabel.Text = "00:00:00";
            statusLabel.Text = "예약된 종료 없음";
            return;
        }

        var remaining = shutdownAt.Value - DateTime.Now;
        if (remaining <= TimeSpan.Zero)
        {
            shutdownAt = null;
            timeLabel.Text = "00:00:00";
            statusLabel.Text = "예약된 종료 없음";
            return;
        }

        var hours = (int)remaining.TotalHours;
        timeLabel.Text = $"{hours:00}:{remaining.Minutes:00}:{remaining.Seconds:00}";
        statusLabel.Text = $"종료 예정  {shutdownAt.Value:HH:mm:ss}";
    }

    private static void RunShutdown(string arguments)
    {
        try
        {
            Process.Start(new ProcessStartInfo {
                FileName = "shutdown.exe",
                Arguments = arguments,
                UseShellExecute = false,
                CreateNoWindow = true,
                WindowStyle = ProcessWindowStyle.Hidden
            });
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                $"Windows 종료 명령 실행에 실패했습니다.\n\n{ex.Message}",
                "오류",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
        }
    }
}
