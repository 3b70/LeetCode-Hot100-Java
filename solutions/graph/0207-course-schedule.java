import java.util.*;
class Solution {
    public boolean canFinish(int numCourses,int[][] prerequisites) {
        List<List<Integer>> graph=new ArrayList<>();
        for(int i=0;i<numCourses;i++) graph.add(new ArrayList<>());
        int[] degree=new int[numCourses];
        for(int[] edge:prerequisites) { graph.get(edge[1]).add(edge[0]); degree[edge[0]]++; }
        Queue<Integer> q=new ArrayDeque<>();
        for(int i=0;i<numCourses;i++) if(degree[i]==0) q.offer(i);
        int done=0;
        while(!q.isEmpty()) {
            int u=q.poll(); done++;
            for(int v:graph.get(u)) if(--degree[v]==0) q.offer(v); // 所有前置课已完成
        }
        return done==numCourses;
    }
}
