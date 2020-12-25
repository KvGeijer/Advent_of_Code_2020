import System.IO

solve :: (Int, Int) -> [[Char]] -> Int
solve (y,x) trees = let
        (rows, cols) = (length trees, length $ trees !! 0)
        path = createPath rows x y
        treePath = createTreePath cols trees path
        hits = length . filter (== '#') $ treePath
        in hits

-- Could write point free
realCol :: Int -> Int -> Int
realCol cols col = (mod) col cols

createPath :: Int -> Int -> Int -> [(Int,Int)]
createPath rows x y = [(y*i,x*i) | i <- [0 .. ((div) (rows-1) y)] ]

createTreePath :: Int -> [[Char]] -> [(Int,Int)] -> [Char]
createTreePath cols trees path = [(trees !! row) !! (realCol cols col) | (row,col) <- path]

--main :: IO ()
main = do
        trees <- fmap lines getContents
        
        let  xy = [(1,1), (1, 3), (1, 5), (1, 7), (2, 1)]
             hits = map (flip solve trees) xy
        print $ product hits
        
