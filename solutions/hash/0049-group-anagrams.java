import java.util.*;
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groups = new HashMap<>();
        for (String s : strs) {
            char[] chars = s.toCharArray(); // 新数组可以排序，String 本身不可变
            Arrays.sort(chars);
            String key = new String(chars);
            if (!groups.containsKey(key)) groups.put(key, new ArrayList<>());
            groups.get(key).add(s); // 同一个排序键对应同一组
        }
        return new ArrayList<>(groups.values());
    }
}
