import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.Random;
import java.util.ArrayList;
import java.util.Collections;
import java.io.PrintWriter;

public class TwoOptTsp {
    private int id;
    private long startTime;

    private int cityNb = 0;
    private int[][] graph;

    private ArrayList<Integer> tour = null;

    public int bestPathLength = -1;
    public ArrayList<Integer> bestTour;

    public TwoOptTsp(int _id, int[][] _graph, long _startTime) {
        id = _id;
        graph = _graph;
        startTime = _startTime;
        cityNb = graph.length;
    }

    public int pathLenght() {
        int length = 0;
        for (int i = 0; i < cityNb - 1; i++) {
            length += graph[ tour.get(i) ][ tour.get(i + 1) ];
        }
        return length;
    }

    private void calcOpt() {
        int before_dist;
        int res;

        for (int i = 0; i < cityNb - 1; i++) {
            before_dist = -1;
            res = 0;

            for (int j = i + 1; j < cityNb; j++) {
                int after_dist = graph[ tour.get(i) ][ tour.get(j) ];

                if (before_dist > after_dist || before_dist == -1) {
                    res = j;
                    before_dist = after_dist;
                }
            }

            if (res != 0) {
                int tmp = tour.get(i + 1);
                tour.set(i + 1, tour.get(res));
                tour.set(res, tmp);
            }
        }
    }

    private void initTour() {
        tour.clear();
        bestTour.add(0);
        bestTour.add(0);
        for (int i = 1; i < cityNb; i++) {
            bestTour.add(0);
            tour.add(i);
        }
        Collections.shuffle(tour);
        tour.add(0, 0);
        tour.add(0);
    }

    public void run(long maxDuration) {
        tour = new ArrayList<Integer>();
        bestTour = new ArrayList<Integer>();

        while (startTime + maxDuration > System.currentTimeMillis()) {
            initTour();

            calcOpt();
            
            int len = pathLenght();
            if (len < bestPathLength || bestPathLength == -1) {
                bestPathLength = len;
                for (int i = 0; i < cityNb; i++) {
                    bestTour.set(i, tour.get(i));
                }
            }
        }
    }

    private static int[][] loadData(String path) throws IOException {
        FileReader fr = new FileReader(path);
        BufferedReader buf = new BufferedReader(fr);
        String line;
        int i = 0;
        int j;

        int[][] graph = new int[1000][1000];

        while ((line = buf.readLine()) != null) {
            String splitA[] = line.split(",");
            LinkedList<String> split = new LinkedList<String>();
            for (String s : splitA)
                if (!s.isEmpty())
                    split.add(s);

            j = 0;

            for (String s : split)
                if (!s.isEmpty())
                    graph[i][j++] = Integer.parseInt(s)   ;

            i++;
        }
        return graph;
    }

    public static String tourToString(ArrayList<Integer> bestTour) {
        String t = new String();
        for (int i : bestTour)
            t = t + " " + i;
        return t;
    }

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("HELP: java TwoOptTsp <inputFileName> [outputFileName]");
            return;
        }

        long startTime = System.currentTimeMillis();

        try {
            int[][] graph = loadData(args[0]);

            String outputFileName = "out.txt";
            if (args.length == 2) {
                outputFileName = args[1];
            }

            TwoOptTsp tsp = new TwoOptTsp(0, graph, startTime);
            tsp.run(28000);

            System.out.println("Best tour length: " + tsp.bestPathLength);

            PrintWriter writer = new PrintWriter(outputFileName, "UTF-8");
            for (int i : tsp.bestTour)
                writer.println(i + 1);
            writer.close();

            System.out.println("Duration in ms: " + (System.currentTimeMillis() - startTime));

        } catch (IOException e) {
            System.err.println("Error reading graph.");
            return;
        }
    }
}