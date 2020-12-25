import System.IO
import Data.Array

data Instr = Acc Int | Jmp Int | Nop Int | Err deriving (Show)

main = do
        instructions <- fmap (map toInstr . lines . filter (/= '\r')) getContents
        let     n = length instructions
                swappedInstr = [ swapOne i instructions | i <- [0..n-1]]
                trimmedInstr = trim n swappedInstr
                arrs = map (listArray (1,n)) trimmedInstr
                sols = map isLoop arrs
                sol = fst . head . filter snd $ sols
        print sol

--Trims away unchanged instruction versions
trim :: Int -> [[Instr]] -> [[Instr]]
trim n [] = []
trim n (x:xs) 
        | length x < n  = trim n xs
        | otherwise     = x : trim n xs


swapOne :: Int -> [Instr] -> [Instr]
swapOne 0 (x:xs) = case x of
        Jmp y -> Nop y : xs
        Nop y -> Jmp y : xs
        y -> []
swapOne lin (x:xs) = x : (swapOne (lin -1) xs)


-- Is there an infinite loop in the instructions?
isLoop :: Array Int Instr -> (Int, Bool)
isLoop = exec 1 0 []


exec :: Int -> Int -> [Int] -> Array Int Instr -> (Int,Bool)
exec line acc visited arr = let 
        n = length arr
        in if line > n then (acc,True) else let
                ins = arr ! line 
                in if elem line visited then (acc,False) else case ins of
                        Acc x -> exec (line+1) (acc+x) (line:visited) arr
                        Jmp x -> exec (line+x)  acc    (line:visited) arr
                        Nop x -> exec (line+1)  acc    (line:visited) arr
                        Err   -> (0, False)
        
        
toInstr :: String -> Instr
toInstr str = let 
        ins = take 3 str
        num = read . drop 5 $ str
        signed = if str !! 4 == '-' then -num else num
        in case ins of
                "acc" -> Acc signed
                "jmp" -> Jmp signed
                "nop" -> Nop signed
                xs    -> Err
                