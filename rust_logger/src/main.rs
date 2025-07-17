use chrono::Local; use tokio::sync::Mutex;
use std::{fs::OpenOptions, io::prelude::Write, path::Path, sync::Arc};

#[tokio::main]
async fn main() {
    let dir = Path::new("0server.log");
    let logger = Arc::new(Mutex::new(OpenOptions::new().create(true).append(true).open(dir).unwrap()));
    let lgr = logger.clone();

    let ctx = zmq::Context::new();
    let socket = ctx.socket(zmq::SUB).unwrap();

    match socket.connect("tcp://localhost:5554") {
        Ok(_) => {},
        Err(_)=> {println!("Logger failed"); std::process::exit(-1)}
    }

    let time = Local::now().format("%Y-%m-%dT%H:%M:%SZ");
    let online: String = format!("{time} | INFO  | SYSTEM | Server online\n");
    match socket.set_subscribe(b"") {
        Ok(_) => {
            let mut loggr = lgr.lock().await;
            loggr.write_all(online.as_bytes()).unwrap();
        }
        Err(_)=> {println!("Logger failed"); std::process::exit(-1)}
    }

    let (tx, mut rx) = tokio::sync::mpsc::channel::<String>(100);
    tokio::spawn(async move {
        while let Some(log) = rx.recv().await {
            let time = Local::now().format("%Y-%m-%dT%H:%M:%SZ");
            if log == "Shutting down!" {
                let stop: String = format!("{time} | INFO  | SYSTEM | Server Shutting down\n");
                let mut loggr = lgr.lock().await;
                loggr.write_all(stop.as_bytes()).unwrap();
                break;
            }

            let message: String = format!("{time} | {log}\n");
            let mut loggr = lgr.lock().await;
            loggr.write_all(message.as_bytes()).unwrap();
        }
    });

    loop {
        let log = socket.recv_string(0).unwrap().unwrap();

        match tx.send(log).await {
            Ok(_) => {},
            Err(_) => {
                let time = Local::now().format("%Y-%m-%dT%H:%M:%SZ");
                let errmsg: String = format!("{time} | ERROR | SYSTEM | logger going offline\n");
                let logger = Arc::new(Mutex::new(OpenOptions::new().create(true).append(true).open(dir).unwrap()));

                let mut loggr = logger.lock().await;
                loggr.write_all(errmsg.as_bytes()).unwrap();
                std::process::exit(1)
            }
        }
    }

}
