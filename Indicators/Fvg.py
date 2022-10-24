class Fvg():

    def __init__(self):
        self.fvg_tracker = {
            'delta_p': [],
            'delta_n': [],
        }

    def cycle_chunk(self, chunk):

        print('running check on data')
        # print('Date {}, Open {} , Close, {} , Low, {}, High, {}'.format(chunk.datetime[0], chunk.open[0], chunk.close[0], chunk.low[0], chunk.high[0]))


        for i in range(-300, 1, 1):

            try:
                # Index through all data taking 3 at a time
                print('running check on chunk')
                self.get_movement_delta(chunk, i)
            except Exception as e:
                raise

        print(self.fvg_tracker)


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

    def sanitize_invalidated_value_gaps(self):
        print('sanitizing')

    def profile_value_gap(self):
        print('profiling value gap')

    def get_movement_delta(self, chunk, index) -> int:
        # Signifies bull FVG
        if chunk.high[index] < chunk.low[index+2] and chunk.high[index] > chunk.open[index+1] and chunk.low[index+2] < chunk.close[index+1]:
            self.fvg_tracker['delta_p'].append({
                'fvg_high': chunk.low[index+2],
                'fvg_low': chunk.high[index],
            })
        # Signifies bear FVG
        if chunk.low[index] > chunk.high[index+2] and chunk.low[index] < chunk.open[index+1] and chunk.high[index+2] > chunk.close[index+1]:
            self.fvg_tracker['delta_n'].append({
                'fvg_high': chunk.low[index],
                'fvg_low': chunk.high[index+2]
            })
