package twitterExp.streaming.tweets;


import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
 
import javax.imageio.ImageIO;
import javax.imageio.stream.FileImageOutputStream;
 
/**
 * This program demonstrates how to resize an image.
 *
 * @author www.codejava.net
 *
 */
public class ImageResizer {
 
    /**
     * Resizes an image to a absolute width and height (the image may not be
     * proportional)
     * @param inputImagePath Path of the original image
     * @param outputImagePath Path to save the resized image
     * @param scaledWidth absolute width in pixels
     * @param scaledHeight absolute height in pixels
     * @throws IOException
     */
    public static void resize(String inputImagePath,
            String outputImagePath, int scaledWidth, int scaledHeight)
            throws IOException {
        // reads input image
        File inputFile = new File(inputImagePath);
        BufferedImage inputImage = ImageIO.read(inputFile);
 
        // creates output image
        BufferedImage outputImage = new BufferedImage(scaledWidth,
                scaledHeight, inputImage.getType());
 
        // scales the input image to the output image
        Graphics2D g2d = outputImage.createGraphics();
        g2d.drawImage(inputImage, 0, 0, scaledWidth, scaledHeight, null);
        g2d.dispose();
 
        // extracts extension of output file
        String formatName = outputImagePath.substring(outputImagePath
                .lastIndexOf(".") + 1);
 
        // writes to output file
        ImageIO.write(outputImage, formatName, new File(outputImagePath));
    }
 
    /**
     * Resizes an image by a percentage of original size (proportional).
     * @param inputImagePath Path of the original image
     * @param outputImagePath Path to save the resized image
     * @param percent a double number specifies percentage of the output image
     * over the input image.
     * @throws IOException
     */
    public static void resize(String inputImagePath,
            String outputImagePath, double percent) throws IOException {
        File inputFile = new File(inputImagePath);
        BufferedImage inputImage = ImageIO.read(inputFile);
        int scaledWidth = (int) (inputImage.getWidth() * percent);
        int scaledHeight = (int) (inputImage.getHeight() * percent);
        resize(inputImagePath, outputImagePath, scaledWidth, scaledHeight);
    }
 
    /**
     * Test resizing images
     */
    public static void main(String[] args) {
        String inputImagePath = "/Users/madhav/Desktop/TestData/";
        String outputImagePath1 = "/Users/madhav/Desktop/TestData_Processed/";
        String outputImagePath2 = "D:/Photo/Puppy_Smaller.jpg";
        String outputImagePath3 = "D:/Photo/Puppy_Bigger.jpg";
 
        try {
//        		File fp = new File(outputImagePath1);
//        		fp.createNewFile();
//        		FileImageOutputStream iostream = new FileImageOutputStream(fp);
            // resize to a fixed width (not proportional)
        		File fp = new File(inputImagePath);
        		File[] images = fp.listFiles();
        		File errorFile = new File("/Users/madhav/Desktop/faulty.txt");
        		int count =0;
        		FileWriter err = new FileWriter(errorFile);
        		for(File image: images) {
        			String inpImage = image.getPath();
        			String outImage = outputImagePath1 + inpImage.split("/")[5];
        			int scaledWidth = 400;
        			int scaledHeight = 400;
        			try {
						ImageResizer.resize(inpImage, outImage, scaledWidth, scaledHeight);
					} catch (Exception e) {
						count++;
						System.out.println(count);
						System.out.println(inpImage.split("/")[5]);
						err.write(inpImage.split("/")[5]);
						err.write("\n");
						//e.printStackTrace();
						continue;
					}
        		}
            // resize smaller by 50%
//            double percent = 0.5;
//            ImageResizer.resize(inputImagePath, outputImagePath2, percent);
// 
//            // resize bigger by 50%
//            percent = 1.5;
//            ImageResizer.resize(inputImagePath, outputImagePath3, percent);
// 
        } catch (IOException ex) {
            System.out.println("Error resizing the image.");
            ex.printStackTrace();
        }
    }
 
}