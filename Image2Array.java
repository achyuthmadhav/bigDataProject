package twitterExp.streaming.tweets;

import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import javax.imageio.ImageIO;

import org.bson.BSON;
import org.bson.Document;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.mongodb.BasicDBObject;
import com.mongodb.DBCursor;
import com.mongodb.MongoClient;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoIterable;



public class Image2Array {

	public static void main(String[] args) {
		String inputImagePath = "/Users/madhav/Desktop/TestData_Processed/";
		File tweetSample = new File("testSample.tsv");
		FileReader fr = null;
		try {
			fr = new FileReader(tweetSample);
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		}
		BufferedReader br = new BufferedReader(fr);
		List<String> imageFiles = new ArrayList<String>();
		boolean reading = true;
		while(reading)
		try {
			imageFiles.add(inputImagePath + br.readLine().split("\n")[0] + ".jpg");
		} catch (Exception e1) {
			reading = false;
			e1.printStackTrace();
		}
		int count =0, classCount = 0;
		JSONObject json = null;
		File jsonFile = new File("testData.json");
		FileWriter jsonWrite=null;
		File errorFile = new File("/Users/madhav/Desktop/faulty.txt");
		FileWriter err ;
		try {
			jsonWrite = new FileWriter(jsonFile);
			jsonWrite.write("[");
			err = new FileWriter(errorFile);
		} catch (IOException e1) {
			e1.printStackTrace();
		}
		for(String imageFile : imageFiles) {
			JSONArray imageArray = new JSONArray();
			json = new JSONObject();
			int scaledWidth = 400;
			int scaledHeight = 400;
			try {
				imageArray = Image2Array.toArray(imageFile, scaledWidth, scaledHeight, json);
				String iFileName = imageFile.split("/")[5];
				//json.put("tweet_id",iFileName.substring(0, iFileName.length()-4));
				json.put(iFileName.substring(0, iFileName.length()-4), imageArray);
				classCount++;
				System.out.println(classCount);
			}
			catch (Exception e) {
				count++;
				System.out.println(count);
				System.out.println(imageFile.split("/")[5]);
				e.printStackTrace();
				continue;
			}
		}
		try {
			jsonWrite.write(json.toJSONString());
		} catch (IOException e1) {
			e1.printStackTrace();
		}
		try {
			jsonWrite.write("]");
		} catch (IOException e1) {
			e1.printStackTrace();
		}
//        String outputImagePath1 = "/Users/madhav/Desktop/TestData_Processed/";
//        String outputImagePath2 = "D:/Photo/Puppy_Smaller.jpg";
//        String outputImagePath3 = "D:/Photo/Puppy_Bigger.jpg";
//        try {
////        		File fp = new File(outputImagePath1);
////        		fp.createNewFile();
////        		FileImageOutputStream iostream = new FileImageOutputStream(fp);
//            // resize to a fixed width (not proportional)
//        		File fp = new File(inputImagePath);
//        		File[] images = fp.listFiles();
//        		
//        		
//        		for(File image: images) {
//        		
//        			if(classCount > 80000)
//        				break;
//        			JSONArray imageArray = new JSONArray();
//        			String inpImage = image.getPath();
//        			String outImage = outputImagePath1 + inpImage.split("/")[5];
//        			int scaledWidth = 400;
//        			int scaledHeight = 400;
//        			json = new JSONObject();
//        			try {
//						imageArray = Image2Array.toArray(inpImage, scaledWidth, scaledHeight, json);
//						
//						
//					} catch (Exception e) {
//						
//					}
//        			
//        		}
        		try {
					jsonWrite.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
            // resize smaller by 50%
//            double percent = 0.5;
//            ImageResizer.resize(inputImagePath, outputImagePath2, percent);
// 
//            // resize bigger by 50%
//            percent = 1.5;
//            ImageResizer.resize(inputImagePath, outputImagePath3, percent);
// 
     
	}

	private static JSONArray toArray(String inpImage, int scaledWidth, int scaledHeight, JSONObject json) {
		File inputFile = new File(inpImage);
		Integer[][] arr = null;
		JSONArray arrx = new JSONArray();
		JSONArray arry = null;
		try {
			BufferedImage inputImage = ImageIO.read(inputFile);
			arr = new Integer[scaledWidth][scaledHeight];
			for(int w=0; w<scaledWidth; w++) {
				arry = new JSONArray();
				for(int h=0; h<scaledHeight; h++) {
					arr[w][h] = inputImage.getRGB(w, h);
					arry.add(arr[w][h]);
				}
				arrx.add(arry);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return arrx;
	}

}
