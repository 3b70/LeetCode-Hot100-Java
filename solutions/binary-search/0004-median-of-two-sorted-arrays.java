class Solution {
    public double findMedianSortedArrays(int[] a,int[] b) {
        if(a.length>b.length) return findMedianSortedArrays(b,a);
        int m=a.length,n=b.length,l=0,r=m;
        while(l<=r) {
            int i=l+(r-l)/2,j=(m+n+1)/2-i;
            int al=i==0?Integer.MIN_VALUE:a[i-1],ar=i==m?Integer.MAX_VALUE:a[i];
            int bl=j==0?Integer.MIN_VALUE:b[j-1],br=j==n?Integer.MAX_VALUE:b[j];
            if(al<=br && bl<=ar) { // 两侧交叉边界都满足整体有序
                if((m+n)%2==1) return Math.max(al,bl);
                return ((double)Math.max(al,bl)+Math.min(ar,br))/2;
            }
            if(al>br) r=i-1; else l=i+1;
        }
        throw new IllegalArgumentException("输入必须为有序数组");
    }
}
