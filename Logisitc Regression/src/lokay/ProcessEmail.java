package lokay;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;

public class ProcessEmail {

    public static void main(String[] args) throws Exception {

        String root = "lokay-m";
        String[] dirs = new File(root).list();

        // HashMap<String,Integer> labels = new HashMap<String,Integer>();

        HashSet<String> training_files = new HashSet<String>();
        HashSet<String> testing_files = new HashSet<String>();

        for (int i = 0; i < dirs.length; i++)
            TrainTest(root, dirs[i], training_files, testing_files, true);

        // uncomment this if you want to print out lists of training and testing
        // files
        /*
         * printFileList("processed/train-files.txt", training_files);
         * printFileList("processed/test-files.txt", testing_files);
         */

        Histogram<String> vocabulary = new Histogram<String>();
        HashMap<String, Histogram<String>> trainData = new HashMap<String, Histogram<String>>();

        generateData(root, dirs, vocabulary, trainData, training_files);

        int min_count = 3;
        int most_common = 100;

        // uncomment if you want to see the size of the vocabularies before
        // pruning
        /*
         * System.out.println(vocabulary.keySet().size()); 
         * for (String dir : trainData.keySet()) 
         *    System.out.println(dir + ":" + trainData.get(dir).keySet().size());
         */
        pruneData(vocabulary, trainData, min_count, most_common);

        // uncomment if you want to see the size of the vocabularies after
        // pruning
        /*
         * System.out.println(vocabulary.keySet().size()); 
         * for (String dir : trainData.keySet()) 
         *     System.out.println(dir + ":" + trainData.get(dir).keySet().size());
         */

        // uncomment if you wish to generate the training data files
        /*
         * printHistogram("processed/vocabulary.txt", vocabulary); 
         * for (String dir : trainData.keySet()) 
         *     printHistogram("processed/" + dir + ".train.txt", trainData.get(dir));
         */

        // uncomment if you wish to generate the testing output
        /*
         * PrintWriter out = new PrintWriter(new
         * FileWriter("processed/test.txt")); 
         * for (String dir : trainData.keySet()) { 
         *     for (String instance : generateTesting(root, dir, vocabulary, testing_files)) 
         *         out.println(instance); 
         * }
         * out.close();
         */

        // uncomment if you wish to generate the libsvm output
        /*
        LexiconPair lexicon = generateSVM(root, dirs, vocabulary, training_files, 
                testing_files, false, "libsvm/train.libsvm", "libsvm/test.libsvm");
        printLexicon(lexicon, "libsvm/labels.lexicon", "libsvm/features.lexicon");
     	*/
    }

    public static void printLexicon(LexiconPair lexicon, String labelsFile,
            String featuresFile) throws Exception {
        PrintWriter out = new PrintWriter(new FileWriter(labelsFile));
        for (String key : lexicon.labels.keySet()) {
            out.println(key + " " + lexicon.labels.get(key));
        }
        out.close();
        out = new PrintWriter(new FileWriter(featuresFile));
        for (String key : lexicon.features.keySet()) {
            out.println(key + " " + lexicon.features.get(key));
        }
        out.close();
    }
    
    // note that this is specifically tied to Problem Set 3 with labels
    public static LexiconPair generateSVM(String root, String[] dirs, 
            Histogram<String> vocabulary, HashSet<String> training_files, 
            HashSet<String> testing_files, boolean tf, 
            String trainOutput, String testOutput) throws Exception {
        LexiconPair result = new LexiconPair();
        result.labels = new Lexicon(2);
        result.labels.put(dirs[0], 2);
        result.labels.put(dirs[1], 6);
        result.features = new Lexicon(1);
        PrintWriter trainOut = new PrintWriter(new FileWriter(trainOutput));
        PrintWriter testOut = new PrintWriter(new FileWriter(testOutput));
        for (int i = 0; i < dirs.length; i++) {
            String[] files = new File(root + "/" + dirs[i]).list();
            for (int j = 0; j < files.length; j++) {
                Histogram<Integer> data = new Histogram<Integer>();
                String file = dirs[i] + "/" + files[j];
                BufferedReader br = new BufferedReader(new FileReader(root + "/" + file));
                String line = null;
                while ((line = br.readLine()) != null) {
                    String[] words = process_line(line);
                    for (int k = 0; k < words.length; k++) {
                        if (vocabulary.containsKey(words[k]))
                            data.put(result.features.get(words[k]));
                    }
                }
                br.close();
                PrintWriter out = testOut;
                if (training_files.contains(file))
                    out = trainOut;
                out.print(result.labels.get(dirs[i]) + ".0");
                ArrayList<Integer> features = new ArrayList<Integer>(data.keySet());
                Collections.sort(features);
                for (Integer f : features) {
                    if (tf)
                        out.print(" " + f + ":" + data.get(f) + ".0");
                    else
                        out.print(" " + f + ":1.0");
                }
                out.println();
            }
        }
        trainOut.close();
        testOut.close();
        return result;
    }

    public static void printHistogram(String file, Histogram<String> histogram) throws Exception {
        PrintWriter out = new PrintWriter(new FileWriter(file));
        for (String word : histogram.keySet())
            out.println(word + " " + histogram.get(word));
        out.close();
    }

    public static void printFileList(String file, HashSet<String> files) throws Exception {
        PrintWriter out = new PrintWriter(new FileWriter(file));
        for (String f : files)
            out.println(f);
        out.close();
    }

    public static ArrayList<String> generateTesting(String root, String dir, Histogram<String> vocabulary,
            HashSet<String> testing_files) throws Exception {
        ArrayList<String> result = new ArrayList<String>();
        String[] files = new File(root + "/" + dir).list();
        for (int i = 0; i < files.length; i++) {
            String file = dir + "/" + files[i];
            if (testing_files.contains(file)) {
                StringBuilder instance = new StringBuilder();
                BufferedReader br = new BufferedReader(new FileReader(root + "/" + file));
                String line = null;
                while ((line = br.readLine()) != null) {
                    String[] words = process_line(line);
                    for (int j = 0; j < words.length; j++) {
                        if (vocabulary.containsKey(words[j]))
                            instance.append(words[j]).append(" ");
                    }
                }
                br.close();
                result.add(dir + " " + instance.toString().trim());
            }
        }
        return result;
    }

    public static void pruneData(Histogram<String> vocabulary, HashMap<String, Histogram<String>> training,
            int min_count, int most_common) {
        int max_count = common_threshold(vocabulary, most_common);
        ArrayList<String> keys = new ArrayList<String>(vocabulary.keySet());
        for (String key : keys) {
            if ((vocabulary.get(key).intValue() < min_count) || (vocabulary.get(key).intValue() >= max_count)) {
                // System.out.println("Removing key: " + key);
                vocabulary.remove(key);
                for (String dir : training.keySet())
                    training.get(dir).remove(key);
            }
        }
    }

    public static int common_threshold(Histogram<String> vocabulary, int most_common) {
        Histogram<Integer> totals = new Histogram<Integer>();
        for (String key : vocabulary.keySet())
            totals.put(vocabulary.get(key));
        ArrayList<Integer> counts = new ArrayList<Integer>(totals.keySet());
        Collections.sort(counts);
        // System.out.println(counts);
        int total = 0;
        int index = counts.size() - 1;
        while (total <= 100) {
            total += totals.get(counts.get(index));
            index--;
        }
        return counts.get(index);
    }

    public static void generateData(String root, String[] dirs, Histogram<String> vocabulary,
            HashMap<String, Histogram<String>> training, HashSet<String> training_files) throws Exception {
        for (int i = 0; i < dirs.length; i++) {
            String[] files = new File(root + "/" + dirs[i]).list();
            Histogram<String> trainData = new Histogram<String>();
            for (int j = 0; j < files.length; j++) {
                String file = dirs[i] + "/" + files[j];
                BufferedReader br = new BufferedReader(new FileReader(root + "/" + file));
                String line = null;
                while ((line = br.readLine()) != null) {
                    String[] words = process_line(line);
                    for (int k = 0; k < words.length; k++) {
                        vocabulary.put(words[k]);
                        if (training_files.contains(file))
                            trainData.put(words[k]);
                    }
                }
                br.close();
            }
            training.put(dirs[i], trainData);
        }
    }

    public static void TrainTest(String root, String dir, HashSet<String> training, 
            HashSet<String> testing, boolean debug) throws Exception {
        int train = 0;
        int test = 0;
        String[] files = new File(root + "/" + dir).list();
        for (int i = 0; i < files.length; i++) {
            String file = dir + "/" + files[i];
            BufferedReader br = new BufferedReader(new FileReader(root + "/" + file));
            String line = null;
            boolean found = false;
            while ((line = br.readLine()) != null) {
                if (line.startsWith("Date: ")) {
                    found = true;
                    String[] fields = line.split("\\s+");
                    // String date = fields[3] + "," + fields[4];
                    String date = fields[4];
                    if (Integer.parseInt(date) < 2002) {
                        training.add(file);
                        train++;
                    } else {
                        testing.add(file);
                        test++;
                    }
                    break;
                }
            }
            if (!found) {
                System.out.println("Couldn't find " + file);
                System.exit(1);
            }
            br.close();
        }
        if (debug)
            System.out.println(dir + " training:" + train + " testing:" + test);
    }

    public static String[] process_line(String line) {
        String temp = line.replaceAll("\\.\\s+", " ");
        temp = temp.replaceAll(",\\s+", " ");
        return temp.toLowerCase().split("\\s+");
    }
}
