from Utils import num_func as nf

class Fvg():

    FVG_DELTA_THRESHOLD = 2

    def __init__(self):
        self.fvg_tracker = {
            'delta_p': [],
            'delta_n': [],
        }

    def cycle_chunk(self, chunk):

        for i in range(-600, 1, 1):
            try:
                # Index through all data taking 3 at a time
                self.get_movement_delta(chunk, i)
            except Exception as e:
                raise

        return self.fvg_tracker

        # Compare gradient both directions
        # if we have a criteria met we then check n-1 of n=3 meets following:
        # Negative gradient:
        # low of n=1 is greater than high of n=3 and greater than a set threshold
        # Positive gradient:
        # low of n=3 is higher than high of n=1 and greater than a set threshold
        # Store the locations of the fvg entry and exit price and if theyre + or -
        # Then we will need to findout which of these fvg's have been invalidated
        # Simply look for any closes within data chunk that have either gone over - fvg's
        # or under + fvg's
        # then we look at current time frame and run the following checks/scenarios


    def get_movement_delta(self, chunk, index) -> int:
        # Signifies bull FVG
        if chunk.high[index] < chunk.low[index+2] and chunk.high[index] > chunk.open[index+1] and chunk.low[index+2] < chunk.close[index+1]:
            if nf.pct_delta(chunk.high[index], chunk.low[index+2]) >= self.FVG_DELTA_THRESHOLD:
                self.fvg_tracker['delta_p'].append({
                    'fvg_high': chunk.low[index+2],
                    'fvg_low': chunk.high[index],
                    # 'fvg_timestamp': chunk.datetime[index+2]
                })
        # Signifies bear FVG
        if chunk.low[index] > chunk.high[index+2] and chunk.low[index] < chunk.open[index+1] and chunk.high[index+2] > chunk.close[index+1]:
            if nf.pct_delta(chunk.high[index+2], chunk.low[index]) >= self.FVG_DELTA_THRESHOLD:
                self.fvg_tracker['delta_n'].append({
                    'fvg_high': chunk.low[index],
                    'fvg_low': chunk.high[index+2],
                    # 'fvg_timestamp': chunk.datetime[index+2]
                })
