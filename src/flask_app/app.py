from flask import Flask, jsonify
from boids import boids_gen
from boids.boids_runner import setup_logging


app = Flask(__name__)


@app.route('/boid_positions', methods=['GET'])
def get_boid_positions():
    # Return boid positions for a single time step
    Space.sim_loop()
    return jsonify(Space.boids)

# @app.route('/stream_boid_positions', methods=['GET'])
# def stream_boid_positions():
#     def generate():
#         while True:
#             # Generate boid positions for each time step
#             yield f"data: {json.dumps(boid_positions)}\n\n"
#             time.sleep(1)  # Adjust the sleep time as needed

#     return Response(generate(), mimetype='text/event-stream')



def init_space():
    global Space
    logger = setup_logging()
    logger.info("Starting boids simulation")
    Space = boids_gen.Space()


 
if __name__ == '__main__':
    init_space()
    app.run(debug=True)
