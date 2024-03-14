import { Dialog, Transition } from '@headlessui/react';
import { Formik } from 'formik';
import { Fragment } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import * as Yup from 'yup';
import { ReactComponent as ActivateUserRolesIcon } from '../../../../assets/images/svg/activate-icon.svg';
import { ReactComponent as ModalCloseIcon } from '../../../../assets/images/svg/modal-close-icon.svg';
import useApi from '../../../../hooks/useApi';
import { transformToFormDataOrder } from '../../../../utils/helper';
import {
	closeIsActivateUserModalOpen,
	selectAppApplicationObjectsLogsFormData,
	selectIsActivateUserModalOpen,
	toggleRerenderPage,
} from '../../slice';

const ActivateUserForm = ({ closeModal }) => {
	let { appId } = useParams();
	const dispatch = useDispatch();

	const appApplicationObjectsLogsFormData = useSelector(
		selectAppApplicationObjectsLogsFormData
	);

	const triggerApi = useApi();
	let initialValues = {
		is_active: true,
	};

	let validationSchema = Yup.object({
		is_active: Yup.boolean()
			.required('Required')
			.oneOf([true], 'Activate User'),
	});

	let onSubmit = (values) => {
		let tempValues = values;

		let dynamicFormData = transformToFormDataOrder(tempValues);

		const makeApiCall = async () => {
			const { response, success } = await triggerApi({
				url: `/api/v1/apps/${appId}/users/${appApplicationObjectsLogsFormData?.id}/`,
				type: 'PUT',
				loader: true,
				payload: dynamicFormData,
			});

			if (success && response) {
				closeModal();
				dispatch(toggleRerenderPage());
			}
		};

		makeApiCall();
	};

	return (
		<Formik
			initialValues={initialValues}
			validationSchema={validationSchema}
			onSubmit={onSubmit}
		>
			{(formik) => {
				return (
					<form
						className="complete-hidden-scroll-style flex grow flex-col gap-4 overflow-y-auto"
						onSubmit={formik.handleSubmit}
					>
						<div className="flex grow flex-col gap-[16px]">
							<div className="flex grow flex-col items-center justify-center gap-[16px]">
								<ActivateUserRolesIcon />
								<p className="max-w-[201px] text-center font-lato text-[16px] leading-[24px] tracking-[0.2px] text-[#212429]">
									Sure you want to activate{' '}
									{appApplicationObjectsLogsFormData?.name}?
								</p>
							</div>
							<p className="flex flex-col font-lato text-[14px] leading-[20px] tracking-[0.2px] text-[#212429]">
								<span>Note:</span>
								<span>
									This will enable it and can be disabled anytime later.
								</span>
							</p>
						</div>
						<div className="sticky bottom-0 flex flex-col gap-[8px] bg-[#ffffff] pt-[24px] font-lato text-[#696969]">
							<button
								type="submit"
								className="flex w-full items-center justify-center rounded-[4px] bg-[#229470] px-[16px] py-[10px] font-lato text-[14px] font-bold leading-[20px] text-white disabled:opacity-[0.38]"
							>
								<span>Activate User</span>
							</button>
						</div>
					</form>
				);
			}}
		</Formik>
	);
};

export default function ActivateUserModal() {
	const appApplicationObjectsLogsFormData = useSelector(
		selectAppApplicationObjectsLogsFormData
	);
	const isActivateUserModalOpen = useSelector(selectIsActivateUserModalOpen);
	const dispatch = useDispatch();

	function closeModal() {
		dispatch(closeIsActivateUserModalOpen());
	}

	return (
		<>
			<Transition appear show={isActivateUserModalOpen} as={Fragment}>
				<Dialog as="div" className="relative z-10" onClose={() => {}}>
					<Transition.Child
						as={Fragment}
						enter="ease-in-out duration-700"
						enterFrom="opacity-0"
						enterTo="opacity-100"
						leave="ease-in-out duration-700"
						leaveFrom="opacity-100"
						leaveTo="opacity-0"
					>
						<div className="fixed inset-0 bg-black bg-opacity-[.67]" />
					</Transition.Child>

					<Transition.Child
						as={Fragment}
						enter="transform transition ease-in-out duration-500"
						enterFrom="translate-x-full"
						enterTo="translate-x-0"
						leave="transform transition ease-in-out duration-500"
						leaveFrom="translate-x-0"
						leaveTo="translate-x-full"
					>
						<div className="fixed inset-0 overflow-y-auto">
							<div className="flex h-screen max-h-screen min-h-full grow items-center justify-center text-center md:justify-end">
								<Dialog.Panel className="relative flex h-screen max-h-screen min-h-full w-full max-w-[498px] transform flex-col gap-[32px] overflow-hidden bg-white px-[24px] pt-[52px] pb-[40px] text-left align-middle shadow-xl transition-all md:pl-[32px] md:pr-[72px] md:pt-[32px]">
									<div className="flex justify-end md:absolute md:top-0 md:right-0">
										<button
											type="button"
											className="flex justify-end focus:outline-none md:absolute md:top-[16px] md:right-[16px]"
											onClick={closeModal}
										>
											<ModalCloseIcon />
										</button>
									</div>
									<Dialog.Title as="div" className="flex flex-col gap-2">
										<div className="flex flex-col gap-[2px]">
											<h4 className="font-source-sans-pro text-[22px] font-semibold leading-[28px]">
												Activate {appApplicationObjectsLogsFormData?.name}
											</h4>
										</div>
									</Dialog.Title>
									<ActivateUserForm closeModal={closeModal} />
								</Dialog.Panel>
							</div>
						</div>
					</Transition.Child>
				</Dialog>
			</Transition>
		</>
	);
}
