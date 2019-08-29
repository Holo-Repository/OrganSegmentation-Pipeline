import React, { Component } from "react";

export interface IJobLogTerminalProps {
  jobId: string;
  jobState: string;
}

export interface IJobLogTerminalState {
  lastJobState: string;
  log: string;
}

class JobLogTerminal extends Component<IJobLogTerminalProps, IJobLogTerminalState> {
  state = {
    lastJobState: "",
    log: "Connecting to HoloPipelines service"
  };

  idleIntervalId: any = undefined;

  // TODO: go through server
  jobLogEndpoint = `http://51.105.47.56/api/v1/jobs/${this.props.jobId}/log`;

  render() {
    return (
      <div
        style={{
          height: "250px",
          padding: "20px",
          overflowY: "scroll",
          backgroundColor: "#333",
          color: "#FFB81C",
          fontSize: "small"
        }}
      >
        <pre style={{ overflow: "initial" }}>{this.state.log}</pre>
      </div>
    );
  }

  componentDidMount(): void {
    // Until real log arrives, add "dot dot dot"
    this.idleIntervalId = setInterval(() => {
      this.setState(state => ({ log: state.log + "." }))
    }, 1000);
  }

  componentWillReceiveProps(nextProps: Readonly<IJobLogTerminalProps>): void {
    // Note: This is a deprecated React hook, should be refactored to use more elegant solution
    if (nextProps.jobState !== this.state.lastJobState) {
      console.info(`New state: ${nextProps.jobState} => Updating logs`);
      fetch(this.jobLogEndpoint)
        .then(response => response.text())
        .then(log => {
          // As soon as any real log arrives, stop adding "dot dot dot"
          clearInterval(this.idleIntervalId);
          return this.setState({ log });
        });
    }
  }
}

export default JobLogTerminal;
