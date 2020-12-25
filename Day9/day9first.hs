import System.IO

main = do
        input <- fmap (map read . lines) getContents
        let     sol1 = solve1 input
                sol2 = solve2 input sol1
        print sol2
      
      
solve2 :: [Int] -> Int -> Int
solve2 xs target = let chainLen = contChain xs target in 
        if chainLen >= 0 then maximum (take chainLen xs) + minimum (take chainLen xs) else solve2 (tail xs) target
        

contChain :: [Int] -> Int -> Int
contChain (x:xs) target = if x < target then let res = contChain xs (target - x) in if res > 0 then 1+res else -1
                                else if x == target then 1
                                else -1
    
        
solve1 :: [Int] -> Int
solve1 xs = if success then solve1 (tail xs) else xs !! 25 where
        success = twoAdd (take 25 xs) (xs !! 25)

twoAdd :: [Int] -> Int -> Bool
twoAdd xs target = or [x+y == target | x <- xs, y <- xs]
