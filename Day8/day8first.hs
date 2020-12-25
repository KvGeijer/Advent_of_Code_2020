import System.IO
import Data.Array

data Instr = Acc Int | Jmp Int | Nop | Err deriving (Show)

main = do
        instructions <- fmap (map toInstr . lines . filter (/= '\r')) getContents
        let     n = length instructions
                arr = listArray (1,n) instructions
                sol = exec 1 0 [] arr
        print sol

exec :: Int -> Int -> [Int] -> Array Int Instr -> Int
exec line acc visited arr = let 
        ins = arr ! line 
        in if elem line visited then acc else case ins of
                Acc x -> exec (line+1) (acc+x) (line:visited) arr
                Jmp x -> exec (line+x)  acc    (line:visited) arr
                Nop   -> exec (line+1)  acc    (line:visited) arr
                Err   -> -1 * line
        
        
        
toInstr :: String -> Instr
toInstr str = let 
        ins = take 3 str
        num = read . drop 5 $ str
        signed = if str !! 4 == '-' then -num else num
        in case ins of
                "acc" -> Acc signed
                "jmp" -> Jmp signed
                "nop" -> Nop
                xs    -> Err
                