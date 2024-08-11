using OpenCvSharp;
using OpenCvSharp.Extensions;
using System;
using System.Net.NetworkInformation;
using System.Text;
using System.Text.RegularExpressions;
using ZBar;
using ZXing;
using ZXing.Common;
using ZXing.QrCode;

namespace ClassLibrary1
{
    public class Class1
    {
        public string TurnCamera()
        {
            using (VideoCapture videoCapture = new VideoCapture(0))
            {
                if (!videoCapture.IsOpened())
                {
                    throw new Exception("Unable to open camera");
                }

                QRCodeDetector qrCodeDetector = new QRCodeDetector();
                Mat mat1;

                while (true)
                {
                    Mat frame = new Mat();
                    mat1 = frame;
                    videoCapture.Read(frame);
                    if (!frame.Empty())
                    {
                        Cv2.ImShow("Camera", frame);
                    }


                    if (Cv2.WaitKey(1) == 'q')
                    {
                        break;
                    }
                }
                string masp = null;
                Point2f[] points;
                string result = qrCodeDetector.DetectAndDecode(mat1, out points);
                if (result != null)
                {
                    masp = result;
                }
                Cv2.DestroyAllWindows();
                return masp;
            }
        }
    }
}
