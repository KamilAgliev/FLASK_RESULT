import datetime

from data import db_session
from data.jobs import Jobs
from flask import jsonify
from flask_restful import abort, Resource
from .reqparse_jobs import parser


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not jobs:
        abort(404, message=f"Jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
        return jsonify({'jobs': job.to_dict()})

    def delete(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == job_id).first()
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK - job deleted'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict() for item in jobs]})

    def put(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            end_date=args['end_date'],
            is_finished=bool(args['is_finished']),
            creater_id=args['creater_id'],
            start_date=datetime.datetime.now()
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK - job is added'})
