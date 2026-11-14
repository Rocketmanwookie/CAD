"""Read normalized JSONL stdin and publish fresh physical JointState observations.
Requires ROS 2 Jazzy rclpy/sensor_msgs. Does not publish motion commands.
"""
import argparse
import json
import time
from twin_lab import validate


def main():
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import JointState
    import sys
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--robot-id',required=True);p.add_argument('--model-revision',required=True)
    p.add_argument('--max-age',type=float,default=.25);a=p.parse_args()
    rclpy.init();node=Node('observed_joint_state_adapter')
    pub=node.create_publisher(JointState,'/physical/irb6720/joint_states',10)
    sequence={}
    try:
        for line in sys.stdin:
            try:
                s=validate(json.loads(line))
                age=(time.time_ns()-s['source_time_ns'])/1e9
                if s['robot_id']!=a.robot_id or s['model_revision']!=a.model_revision:raise ValueError('Identity/model mismatch')
                if s['source']!='physical' or s['quality']!='good':raise ValueError('Not good physical data')
                if s['clock_uncertainty_ms']>5 or age+s['clock_uncertainty_ms']/1000>a.max_age or age<-.05:raise ValueError('Stale or clock uncertain')
                key=s['stream_id']
                if s['seq']<=sequence.get(key,-1):raise ValueError('Duplicate or late record')
                sequence[key]=s['seq']
                msg=JointState();msg.header.stamp.sec=s['source_time_ns']//10**9
                msg.header.stamp.nanosec=s['source_time_ns']%10**9
                msg.name=s['joint_names'];msg.position=s['q']
                msg.velocity=s['dq'] or [];msg.effort=s['tau'] or []
                pub.publish(msg);rclpy.spin_once(node,timeout_sec=0)
            except (ValueError,TypeError) as e:node.get_logger().warning(str(e))
    finally:node.destroy_node();rclpy.shutdown()


if __name__=='__main__':main()
