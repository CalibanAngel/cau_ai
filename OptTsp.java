import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.Random;
import java.util.ArrayList;
import java.util.Collections;
import java.io.PrintWriter;

public class OptTsp {
    private int id;
    private long startTime;

    private int totalLen = 0;
    private int[][] graph;

    private ArrayList<Integer> tour = null;

    public int bestTourLength = -1;
    public ArrayList<Integer> bestTour;

    public OptTsp(int _id, int[][] _graph, long _startTime) {
        id = _id;
        graph = _graph;
        startTime = _startTime;
        totalLen = graph.length;
    }

    public int tourLength() {
        int length = 0;
        for (int i = 0; i < totalLen - 1; i++) {
            length += graph[ tour.get(i) ][ tour.get(i + 1) ];
        }
        return length;
    }

    private void calcOpt() {
        int before_dist;
        int res, res2;

        for (int loc = 0; loc < totalLen - 1; loc++) {
            before_dist = -1;
            res = 0;
            res2 = 0;

            for (int loc2 = loc + 1; loc2 < totalLen; loc2++) {

                for (int loc3 = loc2 + 1; loc3 < totalLen; loc3++) {
                    int after_dist = graph[ tour.get(loc) ][ tour.get(loc2) ] + graph[ tour.get(loc2) ][ tour.get(loc3) ];

                    if (before_dist > after_dist || before_dist == -1) {
                        res = loc2;
                        res2 = loc3;
                        before_dist = after_dist;
                    }
                }

            }

            if (res != 0 && res2 != 0) {
                int tmp = tour.get(loc + 1);
                tour.set(loc + 1, tour.get(res));
                tour.set(res, tmp);

                int tmp2 = tour.get(loc + 2);
                tour.set(loc + 2, tour.get(res2));
                tour.set(res2, tmp2);
            }
        }
    }


    public void run(long maxDuration) {
        tour = new ArrayList<Integer>();
        bestTour = new ArrayList<Integer>();

        for (int i = 0; i < totalLen + 1; i++)
            bestTour.add(0);

        while (startTime + maxDuration > System.currentTimeMillis()) {
            tour.clear();
            for (int i = 1; i < totalLen; i++)
                tour.add(i);
            Collections.shuffle(tour);
            tour.add(0, 0);
            tour.add(0);

            calcOpt();
            int len = tourLength();
            if (len < bestTourLength || bestTourLength == -1) {
                bestTourLength = len;
                for (int i = 0; i < totalLen; i++) {
                    bestTour.set(i, tour.get(i));
                }
            }
        }
    }

    public static int[][] loadData(String path) throws IOException {
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
            System.err.println("HELP: java OptTsp <fileName>");
            return;
        }

        long startTime = System.currentTimeMillis();

        try {
            int[][] graph = loadData(args[0]);

            OptTsp tsp = new OptTsp(0, graph, startTime);
            tsp.run(28000);

            System.out.println("Best tour length: " + tsp.bestTourLength);

            PrintWriter writer = new PrintWriter("out.txt", "UTF-8");
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